__all__ = ("Checker",)

from collections import deque
from copy import copy

from deduct_alpha.model import Effect, Entity, Generic


class Checker:
    def __init__(self, theory: deque[Effect], entities: list[Entity]) -> None:
        self.theory = theory
        self.entities = entities

        self.state = list[Effect]()

    def check_premise(self, effect: Effect) -> None:
        for i, premise_effect in enumerate(effect.rule.premise):
            hydrated = premise_effect.hydrate(effect.associated)

            # 前提を満たしているかを確認。
            if hydrated not in self.state:
                raise ValueError(f"指定された効果の{i}番目の前提が満たされていません。")

        # エフェクトを適用する。
        if effect.rule.conclusion:
            effect.rule.conclusion
        self.state.append(effect)


    def next(self) -> None:
        effect = self.theory.pop()

        self.check_premise()
