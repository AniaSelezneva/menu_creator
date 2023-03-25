from django.shortcuts import render


def menu_view(request, url=''):
    return render(request, 'main_page.html')
