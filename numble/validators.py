from collections import Counter

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class MultiValidator:
    """
    short-circuit evaluation of validators
    """

    def __init__(self, validators, kwargs: dict):
        self.validators = validators
        self.kwargs = kwargs

    def __call__(self, value):
        for validator in self.validators:
            validator(value, self.kwargs)


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

    def __call__(self, value: str | None, kwargs: dict) -> None:
        value = self.clean(value)
        return super().__call__(value)


def digit_count_validator(value: str, kwargs: dict):
    """
    Validates that counts of each digit in the given string
    are the same as those of the current puzzle

    Args:
        value (str): user's guess to check for validity

    Raises:
         ValidationError: input is an invalid guess due to digit count
    """
    guess_counts = Counter(value)
    number_counts = Counter(kwargs["numbers"])
    for digit, count in number_counts.items():
        if guess_counts[digit] != count:
            raise ValidationError(
                message="You must use each number exactly once", code="digit_counts"
            )


def correct_answer_validator(value: str, kwargs: dict):
    """
    Validates that given string evaluates to the same value as the answer to the current puzzle

    Args:
        value (str): user's guess to check for validity

    Raises:
        ValidationError: input is unable to be evaluated as a python expression due to bad synta
        ValidationError: input is an invalid guess due to digit count
    """

    # for security reasons, format of string must be strictly checked before calling `eval`
    NoParenRegexValidator(  # pylint: disable=unnecessary-dunder-call
        regex="([1-9][-+*\/x%]){3}[1-9]", message="Congrats, you found a bug!", code="invalid_other"
    ).__call__(value, kwargs)

    value = value.replace("x", "*")
    value = value.replace("%", "/")
    try:
        answer = eval(value, {})
    except SyntaxError as exc:
        raise ValidationError(message="Bad syntax", code="python_syntax") from exc

    if answer != kwargs["target"]:
        raise ValidationError(
            message="%(answer) i is the wrong answer",
            code="wrong_answer",
            params={"answer": answer},
        )
