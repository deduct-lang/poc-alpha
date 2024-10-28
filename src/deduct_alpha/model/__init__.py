from __future__ import annotations

__all__ = ("Entity", "Generic", "Anything", "Effect", "Rule")

from copy import copy
from dataclasses import dataclass


@dataclass
class Entity:
    pass


type Generic = str
Anything = Generic | Entity


@dataclass
class Effect:
    rule: Rule
    associated: dict[Generic, Anything]

    def __post_init__(self) -> None:
        for generic in self.associated:
            if generic not in self.rule.generics:
                raise ValueError("関連付けられたジェネリックは規則で使われていません。")

    def __eq__(self, object: object) -> bool:
        if not isinstance(object, Effect):
            return False

        return self.rule == object.rule and self.associated == object.associated

    def hydrate(self, context: dict[Generic, Anything]) -> Effect:
        hydrated = copy(self)

        # 効果に設定されているジェネリクスに、新しい値を適用する。
        for generic, value in context.items():
            for key in hydrated.associated.keys():
                if hydrated.associated[key] == generic:
                    hydrated.associated[key] = value

        return hydrated


@dataclass
class Rule:
    generics: list[Generic]
    premise: list[Effect]
    conclusion: list[Effect]
