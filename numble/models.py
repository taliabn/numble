import itertools
import random
from collections import namedtuple
from datetime import datetime, timedelta, timezone

Level = namedtuple("Level", ["rating", "numbers", "target", "solutions"])


class Puzzle:
    """
    generates today's puzzle
    """

    def __init__(self) -> None:
        self.operations = ["+", "-", "/", "*"]
        # timezone is UTC
        numble_start_day = datetime(
            2023, 8, 29, tzinfo=timezone(timedelta(hours=0))
        )  # date of numble's initial deployment
        today = datetime.now(tz=timezone(timedelta(hours=0)))
        self.puzzle_day = str((today - numble_start_day).days + 1)
        self.curr_time = today.strftime("%Y%m%d")
        # solutions, numbers, and levels will be set by create_puzzle
        self.soln_map = {}
        self.numbers = None
        self.levels = {}
        self.create_and_set_puzzles()

    def create_and_set_puzzles(self) -> None:
        """
        sets numbers, target, and solutions for the daily puzzle
        """
        random.seed(self.curr_time)
        self.numbers = [str(random.randint(1, 9)) for i in range(4)]
        self.generate_all_puzzles()
        self.choose_puzzles()

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

    def choose_puzzles(self) -> None:
        """
        picks random target, solutions pair from puzzles dictionary
        """
        sorted_targets = list(self.soln_map.keys())
        sorted_targets.sort(reverse=True, key=lambda x: len(self.soln_map[x]))
        length = len(self.soln_map)
        easy_target = random.choice(sorted_targets[: (length * 15) // 100])
        medium_target = random.choice(sorted_targets[(length * 35) // 100 : (length * 65) // 100])
        hard_target = random.choice(sorted_targets[(length * 90) // 100 :])
        for target, difficulty in zip(
            [easy_target, medium_target, hard_target], ["easy", "medium", "hard"]
        ):
            self.levels[difficulty] = Level(difficulty, self.numbers, target, self.soln_map[target])

    def refresh(self) -> None:
        """
        check if the day has changed (in UTC timezone),
        and generate a new puzzle if so
        """
        today = datetime.now(tz=timezone(timedelta(hours=0))).strftime("%Y%m%d")
        if today != self.curr_time:
            self.curr_time = today
            self.generate_all_puzzles()
            self.choose_puzzles()
