from django import forms

from .models import Puzzle


class GuessForm(forms.Form):
    """
    The form the user will use to enter their answer to the puzzle
    Args:
            None
    """

    numbers = Puzzle.numbers
    guess = forms.CharField(label="guess", max_length=30)
