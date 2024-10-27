from __future__ import annotations

__all__ = ("Entity", "Generic", "Anything", "Effect", "Rule")

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

    def __eq__(self, effect: Effect) -> bool:
        return self.rule == effect.rule and self.associated == effect.associated


@dataclass
class Rule:
    generics: list[Generic]
    premise: list[Effect]
    conclusion: list[Effect]
