from dataclasses import asdict, is_dataclass
import textwrap
from typing import Any, Iterable, cast


def pretty_print(obj: Any, max_depth: int | None = None):
    result = format_object(obj, 0, max_depth)
    print("\n" + result)


def indent(values: Iterable[str], p: str) -> str:
    text = textwrap.indent("\n".join(values), "  ", lambda _: True)
    return f"{p[0]}\n{text}\n{p[1]}"


def format_object(obj: Any, depth: int, max_depth: int | None):
    if max_depth is not None and depth > max_depth:
        return f"{obj}"
    if is_dataclass(obj):
        o: Any = obj
        obj = asdict(o)

    def fmt(value: Any) -> str:
        return format_object(value, depth + 1, max_depth)

    match obj:
        case dict():
            obj = cast(dict[Any, Any], obj)
            return indent((f"{k}: {fmt(v)}" for k, v in obj.items()), "{}")
        case list():
            obj = cast(list[Any], obj)
            return indent((fmt(v) for v in obj), "[]")
        case tuple():
            obj = cast(tuple[Any, ...], obj)
            return indent((fmt(v) for v in obj), "()")
        case set():
            obj = cast(set[Any], obj)
            return indent((fmt(v) for v in obj), "{}")
        case _:
            return f"{obj}"
