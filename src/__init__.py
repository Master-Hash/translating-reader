from functools import lru_cache
from typing import List

from deep_translator import GoogleTranslator
from rich.console import RenderableType
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.reactive import Reactive, reactive
from textual.widgets import Footer, Header, Static


@lru_cache
def cached_translate(s: str) -> str:
    return GoogleTranslator(target="zh-CN").translate(s)


def batch_translate(s: List[str]) -> List[str]:
    return [cached_translate(i) for i in s]


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
    sent_data = reactive([""])
    show_translated = reactive(False)

    def action_next_page(self):
        self.page = self.page + 1 if self.page < 41 else 41

    def action_previous_page(self):
        self.page = self.page - 1 if self.page > 1 else 1

    def action_translate(self):
        self.show_translated = not self.show_translated

    def compute_data(self):
        with open(f"./chapters/{self.page}.txt", "r") as f:
            r = f.read().split("\n\n")
            r = [s.replace("\n", " ") for s in r]
        return r

    def compute_translated_data(self):
        return (
            ["" for _ in range(len(self.data))]
            if not self.show_translated
            else [f"\n\n{i}" for i in batch_translate(self.data)]
        )

    def compute_sent_data(self):
        return (f"{i}{j}" for i, j in zip(self.data, self.translated_data))

    def watch_sent_data(self, value: list[str]):
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
