from datetime import datetime
from textual.app import App, ComposeResult
import textual.widgets as wd
import subprocess
from textual import work
from rich.text import Text
from textual.containers import Container

disabled = False

def parse_weather(original):
    lines = original.split('\n')

    cutIndex = 0
    for i, line in enumerate(lines):
        if "6    12    18" in line:
            cutIndex = i
            break

    new = lines[:cutIndex + 1]

    new.append("└────────────────────────────────────────────────────────────────────────┘")

    return '\n'.join(new)

class Weather(wd.Static):
    def on_mount(self) -> None:
        self.load_weather()

    @work(exclusive=True, thread=True)
    def load_weather(self) -> None:
        out = parse_weather(subprocess.run(
            ["curl", "-s", "v2.wttr.in/?m0"],
            capture_output=True, text=True
        ).stdout)
        self.app.call_from_thread(self.update, Text.from_ansi(out))

class WeatherContainer(Container):
    def compose(self) -> ComposeResult:
        yield Weather()

# Real time clock on center
class Clock_container(Container):
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
        yield Clock_container()

class DashboardApp(App):
    CSS = """
    Clock_container {
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
    
        """

    BINDINGS = [("q", "quit", "Exit")]
    def compose(self) -> ComposeResult:
        yield wd.Header()
        with wd.TabbedContent():
            with wd.TabPane("Home"):
                yield Home()
            with wd.TabPane("Weather"):
                yield WeatherContainer()
        yield wd.Footer()

        #event.button.id

if __name__ == "__main__":
    app = DashboardApp()
    app.run()