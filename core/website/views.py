from django.shortcuts import render
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'website/index.html'

class AboutView(TemplateView):
    template_name = 'website/about.html'

def error_404(request, exception):
    return render(request, 'errors/error-404.html', status=404)

def error_500(request):
    return render(request, 'errors/error-500.html', status=500)