from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

# Create your views here.
def homepage(request):
    #return HttpResponse("hello")
    #return render(request, '../templates/index.html')
    return render(request, 'homepage/home.html')
"""
def request_page(request):
    if(request.GET.get('mybtn')):

 return render(request, 'homepage/home2.html')
"""