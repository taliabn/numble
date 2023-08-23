from django.shortcuts import render

from .forms import GuessForm


def index(request):
    """
    generates home view for app

    Args:
            request (HTTPResponse): django HTTP request

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
    return render(request, template_name="mathapp/index.html", context=context)
