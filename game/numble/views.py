from django.shortcuts import render

from .forms import GuessForm
from .models import puzzle


def index(request):
    """
    generates home view for app

    Args:
        request (HTTPResponse): django's built-in base class to inherit from

    Returns:
            None
    """
    if request.method == "POST":
        form = GuessForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = GuessForm()
    context = {"form": form}
    return render(request, template_name="numble/index.html", context=context)
