from io import TextIOWrapper

from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from .forms import VerifySchedule
from .parser import parseCourses, parseCoursesFromPath, parsePeople, parsePeopleFromPath

# Create your views here.


def index(request):
    return render(request, 'scheduler/index.html')


def verifySchedule(request):
    if request.method == 'POST':
        form = VerifySchedule(request.POST, request.FILES)
        if form.is_valid():
            courses = form.cleaned_data['courses']
            schedule = form.cleaned_data['schedule']
            # Have to do a separate case for when it's a tmp file and when it's already in memory
            if courses and isinstance(courses, TemporaryUploadedFile):
                parseCoursesFromPath(courses.temporary_file_path())
            elif courses and isinstance(courses, InMemoryUploadedFile):
                f = TextIOWrapper(courses.file, encoding=request.encoding)
                parseCourses(f)

            if schedule and isinstance(schedule, TemporaryUploadedFile):
                parsePeopleFromPath(schedule.temporary_file_path())
            elif schedule and isinstance(schedule, InMemoryUploadedFile):
                f = TextIOWrapper(schedule.file, encoding=request.encoding)
                parsePeople(f)

            print(courses, schedule)
        else:
            print(form.errors)
        return HttpResponse("hi")
    raise Http404()
