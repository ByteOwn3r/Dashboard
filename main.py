from datetime import datetime
from textual.app import App, ComposeResult
import textual.widgets as wd
import subprocess
from textual import work
from rich.text import Text
from textual.containers import Container

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
        yield wd.Footer()

        #event.button.id

if __name__ == "__main__":
    app = Dashboard()
    app.run()