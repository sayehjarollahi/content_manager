from django.shortcuts import render


def create_library(request):
    return render(request, 'create_library.html')
