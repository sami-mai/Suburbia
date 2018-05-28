from django.shortcuts import render
from suburb.forms import EditSuburbForm


# Create your views here.
def landing(request):
    title = "Home"
    form_class = EditSuburbForm()
    username = request.user.username
    context = {
        "title": title,
        "form_class": form_class,
        "username": username,
    }

    return render(request, 'landing.html', context)
