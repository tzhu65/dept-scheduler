from django.http import HttpResponse, Http404
from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'scheduler/index.html')


def verifySchedule(request):
    if request.method == 'POST':
        print(request.FILES)
        return HttpResponse("hi")
    raise Http404()
