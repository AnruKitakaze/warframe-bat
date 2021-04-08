from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Bat home page</h1>')


def about(request):
    return HttpResponse('<h1>This is for About Page in future</h1>')
