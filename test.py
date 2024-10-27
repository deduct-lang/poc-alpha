from collections import deque

from deduct_alpha import Checker
from deduct_alpha.model import Effect, Entity, Rule

having = Rule(["S", "O"], [], [])
give = Rule(
    ["X", "Y", "O"],
    [Effect(having, {"S": "X", "O": "O"})],
    [Effect(having, {"S": "Y", "O": "O"})],
)

takagi = Entity()
cat = Entity()
marisa = Entity()

theory = deque(
    (
        Effect(having, {"S": takagi, "O": cat}),
        Effect(give, {"X": takagi, "Y": marisa, "O": cat}),
    )
)
Checker(theory, [takagi, cat, marisa])
