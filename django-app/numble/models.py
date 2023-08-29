import itertools
import random
from datetime import datetime, timedelta, timezone


class Puzzle:
    """
    generates today's puzzle
    """

    def __init__(self) -> None:
        self.operations = ["+", "-", "/", "*"]
        date_string = datetime.now(tz=timezone(timedelta(hours=5))).strftime("%Y%m%d")
        random.seed(date_string)
        self.numbers = [str(random.randint(1, 9)) for i in range(4)]

        self.generate_all_puzzles()
        self.choose_puzzle()

    def generate_all_puzzles(self) -> None:
        """
        runs algorithm to generate all possible combinations of today's numbers
        """
        ops = [
            lambda l, r: l + "-" + r,
            lambda l, r: l + "+" + r,
            lambda l, r: l + "*" + r,
            lambda l, r: l + "/" + r,
        ]
        self.soln_map = {}
        res_list = []

        for perm in itertools.permutations(self.numbers):
            for op1, op2, op3 in itertools.product(ops, repeat=3):
                # (a + b) + (c + d)
                res_list.append(
                    op2("(" + op1(perm[0], perm[1]) + ")", "(" + op3(perm[2], perm[3]) + ")")
                )
                # ((a + b) + c)) + d
                res_list.append(
                    op3("(" + op2("(" + op1(perm[0], perm[1]) + ")", perm[2]) + ")", perm[3])
                )
                # (a + (b + c)) + d
                res_list.append(
                    op3("(" + op1(perm[0], "(" + op2(perm[1], perm[2]) + ")") + ")", perm[3])
                )
                # a + ((b + c) + d)
                res_list.append(
                    op1(perm[0], "(" + op3("(" + op2(perm[1], perm[2]) + ")", perm[3] + ")"))
                )
                # a + (b + (c + d))
                res_list.append(
                    op1(perm[0], "(" + op3(perm[1], "(" + op2(perm[2], perm[3]) + ")") + ")")
                )

        for res in res_list:
            try:
                res_number = eval(res)
            except ZeroDivisionError:
                pass
            if not res_number % 1 and 0 < res_number < 100:  # only keep positive ints
                if res_number in self.soln_map:
                    self.soln_map[int(res_number)].append(res)
                else:
                    self.soln_map[int(res_number)] = [res]

    def choose_puzzle(self) -> None:
        """
        picks random target, solutions pair from puzzles dictionary
        """
        self.target = random.choice(list(self.soln_map.keys()))
        self.solutions = self.soln_map[self.target]
