from django import forms

from .validators import (
    MultiValidator,
    NoParenRegexValidator,
    correct_answer_validator,
    digit_count_validator,
)


class GuessForm(forms.Form):
    """
    The form for the user to enter their answer to the puzzle

    Args:
        forms (Form): django's base class to inherit from
    """

    def __init__(self, *args, **kwargs):
        level = kwargs.pop("level")  # Level named tuple
        super().__init__(*args, **kwargs)
        self.fields["guess"] = forms.CharField(
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
                            regex=f"^[{level.numbers[0]}{level.numbers[1]}\
                                	  {level.numbers[2]}{level.numbers[3]}\-+*\/]*$",
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
                    {"numbers": level.numbers, "target": level.target},
                ),
            ],
        )
