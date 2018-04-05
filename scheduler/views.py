from io import TextIOWrapper

from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from .forms import VerifySchedule
from .parser import parseCourses, parseCoursesFromPath, parsePeople, parsePeopleFromPath, parseFacultyHours, parseFacultyHoursFromPath
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
            faculty = form.cleaned_data['faculty']
            print("===================")
            print(courses,people,faculty)
            # Have to do a separate case for when it's a tmp file and when it's already in memory
            if courses and isinstance(courses, TemporaryUploadedFile):
                courses = parseCoursesFromPath(courses.temporary_file_path())
            elif courses and isinstance(courses, InMemoryUploadedFile):
                f = TextIOWrapper(courses.file, encoding=request.encoding)
                courses = parseCourses(f)

            if people and isinstance(people, TemporaryUploadedFile):
                people = parsePeopleFromPath(people.temporary_file_path())
            elif people and isinstance(people, InMemoryUploadedFile):
                f = TextIOWrapper(people.file, encoding=request.encoding)
                people = parsePeople(f)

            if faculty and isinstance(faculty, TemporaryUploadedFile):
                facultyHours = parseFacultyHoursFromPath(faculty.temporary_file_path())
            elif faculty and isinstance(faculty, InMemoryUploadedFile):
                f = TextIOWrapper(faculty.file, encoding=request.encoding)
                facultyHours = parseFacultyHours(f)
            check(courses, people, facultyHours)
        else:
            print("Error with form")
            print(form.errors)
        return HttpResponse("hi")
    raise Http404()
