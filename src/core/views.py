
from django.shortcuts import render

# Create your views here.


def public(request):
    return render(request, 'public.html', {})
