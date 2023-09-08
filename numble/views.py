from django.shortcuts import render

from .forms import GuessForm
from .models import Puzzle

puzzle = Puzzle()


def index(request, difficulty="easy"):
    """
    generates home view for app

    Args:
        request (HTTPResponse): django's built-in base class to inherit from

    Returns:
            None
    """
    puzzle.refresh()
    level = puzzle.levels[difficulty]
    context = {
        "form": GuessForm(level=level),
        "level": level,
        "operations": puzzle.operations,
        "puzzle_day": puzzle.puzzle_day,
        "difficulty": difficulty,
    }
    if request.method == "POST":
        form = GuessForm(request.POST, level=level)
        context["form"] = form
        if form.is_valid():
            return render(request, template_name="numble/win.html", context=context)
    return render(request, template_name="numble/index.html", context=context)
