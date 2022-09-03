from typing import Any

LEVEL = {
    "SUCCESS": "#0ed145",
    "TRACE": "#00a8f3",
    "INFO": "black",  # 背景是白色，所以用黑色
    "WARNING": "yellow",
}


def Size(var: Any, size: int) -> str:
    return f"[size={size}]{var}[/size]"


def Color(var: Any, color: str) -> str:
    return f"[color={color}]{var}[/color]"


def Bold(var: Any) -> str:
    return f"[b]{var}[/b]"


def Link(var: Any) -> str:
    return Color(var, "blue")


def Error(var: Any) -> str:
    return Color(var, "#ec1c24")


def Yellow(var: Any) -> str:
    return Color(var, "#fff344")


def Command(var: Any) -> str:
    return Color(var, "orange")


def Path(var: Any) -> str:
    return Color(var, "#b97a56")


def Quote(var: Any) -> str:
    return Color(var, "grey")


def Log(content: Any, level: str, module: str) -> str:
    return Size(
        (
            f"[{Color(level, LEVEL[level])}] "
            f"{Color(module, LEVEL['TRACE'])} | {content}"
        ),
        18,
    )


def Exercise(name: str) -> str:
    return Size(f"练习{name}：", 40)
