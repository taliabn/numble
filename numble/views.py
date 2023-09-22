from django.shortcuts import redirect, render

from .forms import GuessForm
from .models import Puzzle

puzzle = Puzzle()


def index(request, difficulty):
    """
    generates home view for app

    Args:
        request (HTTPResponse): django's built-in base class to inherit from

    Returns:
            None
    """
    puzzle.refresh()
    level = puzzle.levels[difficulty]
    if difficulty == "easy":
        next_difficulty = "medium"
    elif difficulty == "medium":
        next_difficulty = "hard"
    else:
        next_difficulty = "easy"
    context = {
        "form": GuessForm(level=level),
        "level": level,
        "operations": puzzle.operations,
        "puzzle_day": puzzle.puzzle_day,
        "difficulty": difficulty,
        "next_difficulty": next_difficulty,
    }
    if request.method == "POST":
        form = GuessForm(request.POST, level=level)
        context["form"] = form
        if form.is_valid():
            return render(request, template_name="numble/win.html", context=context)
    return render(request, template_name="numble/index.html", context=context)


def redirect_view(request):  # pylint: disable=unused-argument
    """
    redirects to home view with difficulty set to easy

    Args:
        request (HTTPResponse): django's built-in base class to inherit from

    Returns:
            None
    """
    response = redirect("index", difficulty="easy")
    return response
