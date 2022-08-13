from abc import abstractmethod
import collections
import functools
from typing import Any, Callable, Generic, Iterable, List, Tuple, Type, TypeVar, overload


T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")


class Result(Generic[T, E]):
    @abstractmethod
    def is_ok(self) -> bool:
        ...

    @abstractmethod
    def is_ok_and(self, fn: Callable[[T], bool]) -> bool:
        ...

    @abstractmethod
    def is_err(self) -> bool:
        ...

    @abstractmethod
    def is_err_and(self, fn: Callable[[E], bool]) -> bool:
        ...

    @abstractmethod
    def ok(self) -> "Option[T]":
        ...

    @abstractmethod
    def err(self) -> "Option[T]":
        ...

    @abstractmethod
    def map(self, fn: Callable[[T], U]) -> "Result[U, E]":
        ...

    @abstractmethod
    def map_or(self, default: U, fn: Callable[[T], U]) -> U:
        ...

    @abstractmethod
    def map_or_else(self, default: Callable[[], U], fn: Callable[[T], U]) -> U:
        ...

    @abstractmethod
    def map_err(self, fn: Callable[[E], U]) -> "Result[T, U]":
        ...

    @abstractmethod
    def inspect(self, fn: Callable[[T], None]) -> "Result[T, E]":
        ...

    @abstractmethod
    def inspect_err(self, fn: Callable[[E], None]) -> "Result[T, E]":
        ...

    @abstractmethod
    def expect(self, msg: str) -> T:
        ...

    @abstractmethod
    def unwrap(self) -> T:
        ...

    @abstractmethod
    def expect_err(self, msg: str) -> E:
        ...

    @abstractmethod
    def unwrap_err(self) -> E:
        ...


class Ok(Result[T, E]):
    __match_args__ = ("value",)

    def __init__(self, value: T):
        self.value = value

    def is_ok(self):
        return True

    def is_ok_and(self, fn: Callable[[T], bool]):
        return fn(self.value)

    def is_err(self):
        return False

    def is_err_and(self, _):
        return False

    def ok(self):
        return Some(self.value)

    def err(self):
        return Nothing()

    def map(self, fn: Callable[[T], U]):
        self.value = fn(self.value)
        return self

    def map_or(self, _, fn: Callable[[T], U]):
        return fn(self.value)

    def map_or_else(self, _, fn: Callable[[T], U]):
        return fn(self.value)

    def map_err(self, _):
        return self

    def inspect(self, fn: Callable[[T], None]):
        fn(self.value)
        return self

    def inspect_err(self, _):
        return self

    def expect(self, _):
        return self.value

    def unwrap(self):
        return self.value

    def expect_err(self, msg: str):
        raise Panic(msg)

    def unwrap_err(self):
        raise Panic()

    def __repr__(self) -> str:
        return f"Ok({repr(self.value)})"

    def __lt__(self, other):
        match other:
            case Ok(value):
                return self.value.__lt__(value)
            case Err(_):
                return True
            case _:
                return super().__lt__(other)

    def __le__(self, other):
        match other:
            case Ok(value):
                return self.value.__le__(value)
            case Err(_):
                return True
            case _:
                return super().__le__(other)

    def __eq__(self, other):
        match other:
            case Ok(value):
                return self.value.__eq__(value)
            case Err(_):
                return False
            case _:
                return super().__eq__(other)


class Err(Result[T, E]):
    __match_args__ = ("error",)

    def __init__(self, error: E):
        self.error = error

    def is_ok(self):
        return False

    def is_ok_and(self, _):
        return False

    def is_err(self):
        return True

    def is_err_and(self, fn: Callable[[E], bool]):
        return fn(self.error)

    def ok(self):
        return Nothing()

    def err(self):
        return Some(self.error)

    def map(self, _):
        return self

    def map_or(self, default: U, _) -> U:
        return default

    def map_or_else(self, default: Callable[[], U], _) -> U:
        return default()

    def map_err(self, fn: Callable[[E], U]):
        self.error = fn(self.error)
        return self

    def inspect(self, _):
        return self

    def inspect_err(self, fn: Callable[[E], None]):
        fn(self.value)
        return self

    def expect(self, msg: str):
        raise Panic(msg)

    def unwrap(self):
        raise Panic()

    def expect_err(self, _):
        return self.error

    def unwrap_err(self):
        return self.error

    def __repr__(self) -> str:
        return f"Err({repr(self.error)})"

    def __lt__(self, other):
        match other:
            case Ok(_):
                return False
            case Err(error):
                return self.error.__lt__(error)
            case _:
                return super().__lt__(other)

    def __le__(self, other):
        match other:
            case Ok(_):
                return False
            case Err(error):
                return self.error.__le__(error)
            case _:
                return super().__le__(other)

    def __eq__(self, other):
        match other:
            case Ok(_):
                return False
            case Err(error):
                return self.error.__eq__(error)
            case _:
                return super().__eq__(other)

    def __bool__(self):
        return bool(self.value)


class Option(Generic[T]):
    @abstractmethod
    def is_some(self) -> bool:
        ...

    @abstractmethod
    def is_some_and(self, fn: Callable[[T], bool]) -> bool:
        ...

    @abstractmethod
    def is_nothing(self) -> bool:
        ...

    @abstractmethod
    def expect(self, msg: str) -> T:
        ...

    @abstractmethod
    def unwrap(self) -> T:
        ...

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        ...

    @abstractmethod
    def unwrap_or_else(self, fn: Callable[[], T]) -> T:
        ...

    @abstractmethod
    def inspect(self, fn: Callable[[T], None]) -> "Option[U]":
        ...

    @abstractmethod
    def map(self, fn: Callable[[T], U]) -> "Option[U]":
        ...

    @abstractmethod
    def map_or(self, default: U, fn: Callable[[T], U]) -> U:
        ...

    @abstractmethod
    def map_or_else(self, default: Callable[[], U], fn: Callable[[T], U]) -> U:
        ...

    @abstractmethod
    def and_(self, other: "Option[T]") -> "Option[T]":
        ...

    @abstractmethod
    def and_then(self, fn: Callable[[T], "Option[U]"]) -> "Option[U]":
        ...

    @abstractmethod
    def filter(self, predicate: Callable[[T], bool]) -> "Option[T]":
        ...

    @abstractmethod
    def or_(self, other: "Option[T]") -> "Option[T]":
        ...

    @abstractmethod
    def or_else(self, fn: Callable[[], "Option[U]"]) -> "Option[U]":
        ...

    @abstractmethod
    def xor(self, other: "Option[T]") -> "Option[T]":
        ...

    @abstractmethod
    def ok_or(self, err: E) -> "Result[T, E]":
        ...

    @abstractmethod
    def ok_or_else(self, err: Callable[[], E]) -> "Result[T, E]":
        ...


class Some(Option[T]):
    __match_args__ = ("value",)

    def __init__(self, value: T):
        self.value = value

    def is_some(self):
        return True

    def is_some_and(self, fn):
        return fn(self.value)

    def is_nothing(self):
        return False

    def expect(self, _):
        return self.value

    def unwrap(self):
        return self.value

    def unwrap_or(self, _):
        return self.value

    def unwrap_or_else(self, _):
        return self.value

    def inspect(self, fn: Callable[[T], None]):
        fn(self.value)
        return self

    def map(self, fn: Callable[[T], U]):
        return Some(fn(self.value))

    def map_or(self, _, fn: Callable[[T], U]):
        return fn(self.value)

    def map_or_else(self, _, fn: Callable[[T], U]):
        return fn(self.value)

    def and_(self, other: "Option[T]"):
        return other

    def and_then(self, fn: Callable[[T], "Option[U]"]):
        return fn(self.value)

    def filter(self, predicate: Callable[[T], bool]):
        return self if predicate(self.value) else Nothing()

    def or_(self, _):
        return self

    def or_else(self, _):
        return self

    def xor(self, other: "Option[T]"):
        return Nothing() if other.is_some() else self

    def ok_or(self, _):
        return Ok(self.value)

    def ok_or_else(self, _):
        return Ok(self.value)

    def __repr__(self) -> str:
        return f"Some({repr(self.value)})"

    def __lt__(self, other):
        match other:
            case Some(value):
                return self.value.__lt__(value)
            case Nothing():
                return False
            case _:
                return super().__lt__(other)

    def __le__(self, other):
        match other:
            case Some(value):
                return self.value.__le__(value)
            case Nothing():
                return False
            case _:
                return super().__le__(other)

    def __eq__(self, other):
        match other:
            case Some(value):
                return self.value.__eq__(value)
            case Nothing():
                return False
            case _:
                return super().__eq__(other)

    def __bool__(self):
        return bool(self.value)

    def __iter__(self):
        yield self.value


class Nothing(Option):
    def is_some(self):
        return False

    def is_some_and(self, _):
        return False

    def is_nothing(self):
        return True

    def expect(self, msg: str):
        raise Panic(msg)

    def unwrap(self):
        raise Panic()

    def unwrap_or(self, default: T):
        return default

    def unwrap_or_else(self, fn: Callable[[], T]):
        return fn()

    def inspect(self, _):
        return self

    def map(self, _):
        return self

    def map_or(self, default: U, _):
        return default

    def map_or_else(self, default: Callable[[], U], _):
        return default()

    def and_(self, _):
        return self

    def and_then(self, fn: Callable[[T], "Option[U]"]):
        return self

    def filter(self, _):
        return self

    def or_(self, other: "Option[T]") -> "Option[T]":
        return other

    def or_else(self, fn: Callable[[], "Option[U]"]) -> "Option[U]":
        return fn()

    def xor(self, other: "Option[T]"):
        return other

    def ok_or(self, err: E):
        return Err(err)

    def ok_or_else(self, err: Callable[[], E]):
        return Err(err())

    def __repr__(self) -> str:
        return "Nothing"

    def __lt__(self, other):
        match other:
            case Some(_):
                return True
            case Nothing():
                return False
            case _:
                return super().__lt__(other)

    def __le__(self, other):
        match other:
            case Some(_):
                return True
            case Nothing():
                return True
            case _:
                return super().__le__(other)

    def __eq__(self, other):
        match other:
            case Some(_):
                return False
            case Nothing():
                return True
            case _:
                return super().__eq__(other)

    def __bool__(self):
        return bool(None)

    def __iter__(self):
        return


class Panic(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


@functools.singledispatch
def as_option(value):
    return Some(value)


@as_option.register(collections.abc.Callable)
def _(func: Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return as_option(func(*args, **kwargs))

    return wrapper


@as_option.register(type(None))
def _(_: None):
    return Nothing()


@functools.singledispatch
def as_result(bases: Tuple[Type]):

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return Ok(func(*args, **kwargs))
            except Exception as exc:
                if isinstance(exc, bases):
                    return Err(exc)
                else:
                    raise exc

        return wrapper

    return decorator


@as_result.register(collections.abc.Callable)
def _(fn: Callable):
    return as_result((Exception,))(fn)
