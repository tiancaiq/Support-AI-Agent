import time
from collections.abc import Callable
from typing import TypeVar


T = TypeVar("T")


def now_ms() -> float:
    return time.perf_counter() * 1000


def elapsed_ms(start_ms: float) -> float:
    return round(now_ms() - start_ms, 2)


def result_size(result: object) -> int:
    if result is None:
        return 0
    content = getattr(result, "content", result)
    return len(str(content))


def timed(operation: Callable[[], T]) -> tuple[T, float]:
    start_ms = now_ms()
    result = operation()
    return result, elapsed_ms(start_ms)
