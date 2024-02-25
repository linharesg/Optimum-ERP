from django.shortcuts import render

def index(request):
    template_html = 'dashboard.html'
    return render(request, 'dashboard.html')