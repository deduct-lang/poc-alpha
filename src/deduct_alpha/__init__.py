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
            hydrated = copy(effect)

            for generic, anything in premise_effect.associated.items():
                # ジェネリックで使われているものが存在するか確認する。
                match anything:
                    case str() if anything not in effect.rule.generics:
                        raise ValueError(
                            f"指定された効果の{i}番目の前提のジェネリック{generic}には"
                            f"ジェネリック{anything}が渡されましたが、これは存在していません。"
                        )
                    case Entity() if anything not in self.entities:
                        raise ValueError(
                            f"指定された効果の{i}番目の前提のジェネリック{generic}には"
                            f"実体{anything}が渡されましたが、この実体はチェッカーに未設定です。"
                        )

                # ジェネリックを解決する。
                if isinstance(anything, Entity):
                    continue

                hydrated.associated[generic] = effect.associated[generic]

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
