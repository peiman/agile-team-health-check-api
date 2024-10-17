# typings/pytest_assume/plugin.pyi

from typing import Any, Callable, Generator, TypeVar, ContextManager
import pytest

# Define a generic type variable
T = TypeVar("T")

# Define the assume function as a context manager
def assume(condition: bool) -> ContextManager[None]: ...
