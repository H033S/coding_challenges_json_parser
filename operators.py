from __future__ import annotations
from abc import ABC
from typing import Union


class Expression(ABC):
    pass


class ValueExpression(Expression):

    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        return "<{}: Value:[{}]>".format(self.__class__.__name__, self.value)


class ConstantExpression(ValueExpression):

    def __init__(self, value: Union[int, float, str, bool]) -> None:
        assert type(value) in (int, float, str, bool)
        super().__init__(value)


class ObjectExpression(ValueExpression):

    def __init__(self, value: list[FieldExpression]) -> None:
        assert all(type(f) == FieldExpression for f in value)
        super().__init__(value)


class CollectionExpression(ValueExpression):

    def __init__(self, value: list[ObjectExpression]) -> None:
        assert all(type(f) == ObjectExpression for f in value)
        super().__init__(value)


class KeyExpression(ValueExpression):

    def __init__(self, value: str) -> None:
        assert type(value) == str
        super().__init__(value)


class FieldExpression(Expression):

    def __init__(self, key: KeyExpression, value: ValueExpression) -> None:

        assert type(key) == KeyExpression
        assert type(value) in (
            ConstantExpression,
            ObjectExpression,
            CollectionExpression,
        )

        self.key = key
        self.value = value

    def __repr__(self) -> str:
        return "<{}: Key:[{}] Value:[{}]>".format(
            self.__class__.__name__, self.key, self.value
        )
