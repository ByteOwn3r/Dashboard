from datetime import datetime
from textual.app import App, ComposeResult
import textual.widgets as wd
import subprocess, tasks_manager
from textual import work
from rich.text import Text
from textual.containers import Container, Horizontal

tasks = tasks_manager.TaskManager()
command = ["curl", "-s", "v2.wttr.in/Golada?m0&lang=es"]

def parse_weather(original):
    lines = original.split('\n')

    cutIndex = 0
    for i, line in enumerate(lines):
        if "6    12    18" in line:
            cutIndex = i
            break

    new = lines[:cutIndex + 1]

    new.pop(1)
    new.append("└────────────────────────────────────────────────────────────────────────┘")

    return '\n'.join(new)

def parse_precipitations(original):
    lines = original.split('\n')

    cutIndex = 0
    cutIndexTop = 0
    for i, line in enumerate(lines):
        if "6    12    18" in line:
            cutIndexTop = i

        if "│      ──────────────          ──────────────          ──────────────    │" in line:
            cutIndex = i
            break

    new = lines[cutIndexTop-2:cutIndex -1]

    new.insert(0, lines[0])
    new.insert(1,lines[1])
    new.insert(2, lines[3])
    new.append("└────────────────────────────────────────────────────────────────────────┘")

    return '\n'.join(new)


class Tasks(Container):
    def __init__(self):
        super().__init__()
        self.load_tasks()

    def load_tasks(self):
        self.lines = tasks.read_tasks().split("\n")
        self.tasks = []

        for i, line in enumerate(self.lines):
            if "- [ ]" in line:
                self.tasks.append((line.replace("- [ ] ", ""), False, i))
            elif "- [x]" in line:
                self.tasks.append((line.replace("- [x] ", ""), True, i))

    def compose(self) -> ComposeResult:
        with Horizontal(classes="add-task-row"):
            yield wd.Input(placeholder="New task...", id="new_task_input")
            yield wd.Button("Add", id="add_task_button", variant="success")

        for task,done,i in self.tasks:
            with Horizontal():
                yield wd.Checkbox(task, value=done, id=f"task_{i}")
                yield wd.Button("Delete task", id=f"delete_{i}", variant="error")

    def on_checkbox_changed(self, event: wd.Checkbox.Changed) -> None:
        line = int(event.checkbox.id.replace("task_", ""))
        if event.value == True:
            self.lines[line] = self.lines[line].replace("- [ ]", "- [x]")
        else:
            self.lines[line] = self.lines[line].replace("- [x]", "- [ ]")
        tasks.write_tasks("\n".join(self.lines))
    async def on_button_pressed(self, event: wd.Button.Pressed):
        if "delete_" in event.button.id:
            line = int(event.button.id.replace("delete_", ""))
            self.lines.pop(line)
            tasks.write_tasks("\n".join(self.lines))
            self.load_tasks()
            await self.recompose()
        elif event.button.id == "add_task_button":
            input_widget = self.query_one("#new_task_input", wd.Input)
            text = input_widget.value.strip()
            if text:
                self.lines.append(f"- [ ] {text}")
                tasks.write_tasks("\n".join(self.lines))
                input_widget.value = ""
                self.load_tasks()
                await self.recompose()

class Weather(wd.Static):
    def on_mount(self) -> None:
        self.load_weather()

    @work(exclusive=True, thread=True)
    def load_weather(self) -> None:
        out = parse_weather(subprocess.run(
            command,
            capture_output=True, text=True
        ).stdout)
        self.app.call_from_thread(self.update, Text.from_ansi(out))

class WeatherContainer(Container):
    def compose(self) -> ComposeResult:
        yield Weather()

class Rain(wd.Static):
    def on_mount(self) -> None:
        self.load_rain()

    @work(exclusive=True, thread=True)
    def load_rain(self) -> None:
        out = parse_precipitations(subprocess.run(
            command,
            capture_output=True, text=True
        ).stdout)
        self.app.call_from_thread(self.update, Text.from_ansi(out))

class RainContainer(Container):
    def compose(self) -> ComposeResult:
        yield Rain()

class ClockContainer(Container):
    def compose(self) -> ComposeResult:
        yield Clock()

class Clock(wd.Digits):
    def on_mount(self) -> None:
        self.update_time()
        self.set_interval(0.1, self.update_time)

    def update_time(self) -> None:
        now = datetime.now().strftime("%H:%M:%S")
        self.update(now)

class Home(Container):
    def compose(self) -> ComposeResult:
        yield ClockContainer()

class Dashboard(App):
    CSS = """
        ClockContainer {
            align: center top;
        }

        Clock {
            width: auto;
            height: auto;
        }

        WeatherContainer {
            align: center middle;
        }

        Weather {
            width: auto;
            height: auto;
        }
        
        RainContainer {
            align: center middle;
        }

        Rain {
            width: auto;
            height: auto;
        }

        Tasks {
            width: 100%;
            height: auto;
        }
        
        Tasks Horizontal {
            height: auto;
            padding_bottom: 1;
        }
        
        .add-task-row {
            height: 6;
            margin-bottom: 1;
        }
        
        .add-task-row Input {
            width: 6fr;
        }
        
        .add-task-row Button {
            width: 2fr;
        }
        
            """

    BINDINGS = [("q", "quit", "Exit")]
    def compose(self) -> ComposeResult:
        yield wd.Header()
        with wd.TabbedContent():
            with wd.TabPane("Home"):
                yield Home()
            with wd.TabPane("Weather"):
                yield WeatherContainer()
            with wd.TabPane("Precipitations"):
                yield RainContainer()
            with wd.TabPane("Tasks"):
                yield Tasks()
        yield wd.Footer()

        #event.button.id

if __name__ == "__main__":
    app = Dashboard()
    app.run()