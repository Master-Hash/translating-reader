from rich.console import RenderableType
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.reactive import Reactive, reactive
from textual.widgets import Footer, Header, Static


class ReaderView(Static):
    value = Reactive([""])

    def render(self) -> RenderableType:
        return super().render()

    def watch_value(self, value: str):
        self.update("\n\n".join(value))


class Reader(App[None]):
    BINDINGS = [
        ("d", "toggle_dark", "切换主题"),
        ("f", "next_page", "下一章"),
        ("b", "previous_page", "上一章"),
        ("t", "translate", "显示/隐藏翻译"),
    ]

    page = reactive(1)
    data = reactive(["开始阅读"])
    translated_data = reactive([""])

    def action_next_page(self):
        self.page = self.page + 1 if self.page < 41 else 41

    def action_previous_page(self):
        self.page = self.page - 1 if self.page > 1 else 1

    def compute_data(self):
        with open(f"./chapters/{self.page}.txt", "r") as f:
            return f.read().split("\n\n")

    def watch_data(self, value: list[str]):
        r = self.query_one("#reader")
        r.value = value

    def compose(self) -> ComposeResult:
        yield Header()
        # yield ScrollableContainer(ReaderView(id="reader"))
        yield ScrollableContainer(ReaderView(id="reader"))
        yield Footer()


if __name__ == "__main__":
    app = Reader()
    app.run()
