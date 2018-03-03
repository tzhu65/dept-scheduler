from io import TextIOWrapper

from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from .forms import VerifySchedule
from .parser import parseCourses, parseCoursesFromPath, parsePeople, parsePeopleFromPath
from .checker import check

# Create your views here.


def index(request):
    return render(request, 'scheduler/index.html')


def verifySchedule(request):
    if request.method == 'POST':
        form = VerifySchedule(request.POST, request.FILES)
        if form.is_valid():
            courses = form.cleaned_data['courses']
            people = form.cleaned_data['people']
            # Have to do a separate case for when it's a tmp file and when it's already in memory
            if courses and isinstance(courses, TemporaryUploadedFile):
                parseCoursesFromPath(courses.temporary_file_path())
            elif courses and isinstance(courses, InMemoryUploadedFile):
                f = TextIOWrapper(courses.file, encoding=request.encoding)
                parseCourses(f)

            if people and isinstance(people, TemporaryUploadedFile):
                parsePeopleFromPath(people.temporary_file_path())
            elif people and isinstance(people, InMemoryUploadedFile):
                f = TextIOWrapper(people.file, encoding=request.encoding)
                parsePeople(f)

            check(courses, people)
        else:
            print(form.errors)
        return HttpResponse("hi")
    raise Http404()
