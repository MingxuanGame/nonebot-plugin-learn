from pathlib import Path


def set_state(state: str) -> None:
    with open("state.txt", "w", encoding="utf-8") as f:
        f.write(state)


def get_state() -> str:
    file = Path("state.txt")
    if not file.exists():
        set_state("0")
    with open(file, "r", encoding="utf-8") as f:
        return f.read().strip()


STATES = {
    "0": "初识 NoneBot2",
    "1": "插件入门",
    "2": "加载插件",
    "3": "编写一个简单插件",
}
