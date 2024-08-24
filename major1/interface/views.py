from django.shortcuts import render
from .models import endgame

def base(request):
    return render(request, 'base.html')