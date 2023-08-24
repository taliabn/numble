# pylint: disable=anomalous-backslash-in-string
from collections import Counter

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from .models import Puzzle


class MultiValidator:
    """
    short-circuit evaluation of validators
    """

    def __init__(self, validators):
        self.validators = validators

    def __call__(self, value):
        for validator in self.validators:
            validator(value)


class NoParenRegexValidator(RegexValidator):
    """
    Removes parantheses and white space from a string, then calls django's regex validator

    Args:
        RegexValidator (RegexValidator): django's built-in base class to inherit from
    """

    def clean(self, value: str | None):
        """
        Removes parantheses and white space from a string

        Args:
            value (str | None): input to be cleaned

        Returns:
            str: cleaned string
        """
        value = value.replace("(", "")
        value = value.replace(")", "")
        value = value.replace(" ", "")
        value = value.strip()
        return value

    def __call__(self, value: str | None) -> None:
        value = self.clean(value)
        return super().__call__(value)


def digit_count_validator(value: str):
    """
    Validates that counts of each digit in the given string
    are the same as those of the current puzzle

    Args:
        value (str): user's guess to check for validity

    Raises:
         ValidationError: input is an invalid guess due to digit count
    """
    guess_counts = Counter(value)
    number_counts = Counter(Puzzle.numbers)
    for digit, count in number_counts.items():
        if guess_counts[digit] != count:
            raise ValidationError(
                message="You must use each number exactly once", code="digit_counts"
            )


def correct_answer_validator(value: str):
    """
    Validates that given string evaluates to the same value as the answer to the current puzzle

    Args:
        value (str): user's guess to check for validity

    Raises:
        ValidationError: input is unable to be evaluated as a python expression due to bad synta
        ValidationError: input is an invalid guess due to digit count
    """

    # for security reasons, format of string must be strictly checked first
    NoParenRegexValidator(  # pylint: disable=unnecessary-dunder-call
        regex="([1-9][-+*\/]){3}[1-9]", message="Congrats, you found a bug!", code="invalid_other"
    ).__call__(value)

    try:
        answer = eval(value, {})  # pylint: disable=eval-used
    except SyntaxError as exc:
        raise ValidationError(message="Bad syntax", code="python_syntax") from exc

    if str(answer) != Puzzle.target:
        raise ValidationError(
            message="%(answer) i is the wrong answer",
            code="wrong_answer",
            params={"answer": answer},
        )


class GuessForm(forms.Form):
    """
    The form for the user to enter their answer to the puzzle

    Args:
        forms (Form): django's base class to inherit from
    """

    numbers = Puzzle.numbers
    guess = forms.CharField(
        label="cool label",
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
                ]
            ),
        ],
    )
