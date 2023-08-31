from django.shortcuts import render

from .forms import GuessForm
from .models import Puzzle

puzzle = Puzzle()


def index(request):
    """
    generates home view for app

    Args:
        request (HTTPResponse): django's built-in base class to inherit from

    Returns:
            None
    """
    context = {
        "form": GuessForm(puzzle=puzzle),
        "numbers": puzzle.numbers,
        "target": puzzle.target,
        "operations": puzzle.operations,
    }
    if request.method == "POST":
        form = GuessForm(request.POST, puzzle=puzzle)
        context["form"] = form
        if form.is_valid():
            return render(request, template_name="numble/win.html", context=context)
    return render(request, template_name="numble/index.html", context=context)
