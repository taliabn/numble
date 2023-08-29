from django import forms

from .models import Puzzle
from .validators import (
    MultiValidator,
    NoParenRegexValidator,
    correct_answer_validator,
    digit_count_validator,
)

puzzle = Puzzle()


class GuessForm(forms.Form):
    """
    The form for the user to enter their answer to the puzzle

    Args:
        forms (Form): django's base class to inherit from
    """

    numbers = puzzle.numbers
    guess = forms.CharField(
        label="solution",
        max_length=30,
        validators=[
            MultiValidator(
                [
                    NoParenRegexValidator(
                        regex="^[1-9-+*\/]*$",
                        message="The only allowable operations are: + - * /",
                        code="invalid_op",
                    ),
                    NoParenRegexValidator(
                        regex=f"^[{numbers[0]}{numbers[1]}{numbers[2]}{numbers[3]}\-+*\/]*$",
                        message="Using numbers that aren't in today's puzzle is not allowed",
                        code="invalid_num",
                    ),
                    NoParenRegexValidator(
                        regex="^.*[1-9][1-9].*$",
                        message="Concatenating digits is not allowed",
                        inverse_match=True,
                        code="concat_digits",
                    ),
                    NoParenRegexValidator(
                        regex="^.*[-+*\/][-+*\/].*$",
                        message="Concatenating operations is not allowed",
                        inverse_match=True,
                        code="concat_ops",
                    ),
                    digit_count_validator,
                    correct_answer_validator,
                ],
                {"numbers": puzzle.numbers, "target": puzzle.target},
            ),
        ],
    )
