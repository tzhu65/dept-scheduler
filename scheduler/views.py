from io import TextIOWrapper

from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from .forms import VerifySchedule, GenerateSchedule
from .parser import parseCourses, parseCoursesFromPath, parsePeople, parsePeopleFromPath, parseFacultyHours, parseFacultyHoursFromPath, MissingHeaders
from .checker import check
from .generate import generate

# Create your views here.


def index(request):
    return render(request, 'scheduler/index.html')


def verifySchedule(request):
    if request.method == 'POST':
        form = VerifySchedule(request.POST, request.FILES)
        errors = []
        courses = []
        people = []
        facultyHours = []
        if form.is_valid():
            courses = form.cleaned_data['courses']
            people = form.cleaned_data['people']
            faculty = form.cleaned_data['faculty']

            # Have to do a separate case for when it's a tmp file and when it's already in memory
            try:
                if courses and isinstance(courses, TemporaryUploadedFile):
                    courses = parseCoursesFromPath(courses.temporary_file_path())
                elif courses and isinstance(courses, InMemoryUploadedFile):
                    f = TextIOWrapper(courses.file, encoding=request.encoding)
                    courses = parseCourses(f)
            except MissingHeaders as e:
                if len(e.headers) > 5:
                    errors.append("Missing too many headers in the schedule spreadsheet")
                else:
                    errors.append("Missing headers in the schedule spreadsheet: " + str(e.headers))

            try:
                if people and isinstance(people, TemporaryUploadedFile):
                    people = parsePeopleFromPath(people.temporary_file_path())
                elif people and isinstance(people, InMemoryUploadedFile):
                    f = TextIOWrapper(people.file, encoding=request.encoding)
                    people = parsePeople(f)
            except MissingHeaders as e:
                if len(e.headers) > 5:
                    errors.append("Missing too many headers in the TA preferences spreadsheet")
                else:
                    errors.append("Missing headers in the TA preferences spreadsheet: " + str(e.headers))

            try:
                if faculty and isinstance(faculty, TemporaryUploadedFile):
                    facultyHours = parseFacultyHoursFromPath(faculty.temporary_file_path())
                elif faculty and isinstance(faculty, InMemoryUploadedFile):
                    f = TextIOWrapper(faculty.file, encoding=request.encoding)
                    facultyHours = parseFacultyHours(f)
            except MissingHeaders as e:
                if len(e.headers) > 5:
                    errors.append("Missing too many headers in the faculty hours spreadsheet")
                else:
                    errors.append("Missing headers in the faculty hours spreadsheet: " + str(e.headers))
        else:
            errors.append("Invalid form submission")
            print(form.errors)

        # Check if there were any parsing errors
        if len(errors) > 0:
            return JsonResponse({"errors": errors})
        else:
            checkerErrors = check(courses, people, facultyHours[0])
            if len(checkerErrors) > 0:
                return JsonResponse({"errors": checkerErrors})
            else:
                return HttpResponse("checked the schedule")
    raise Http404()


def generateSchedule(request):
    if request.method == 'POST':
        form = GenerateSchedule(request.POST, request.FILES)
        errors = []
        courses = []
        people = []
        faculty = []
        if form.is_valid():
            courses = form.cleaned_data['courses']
            people = form.cleaned_data['people']
            faculty = form.cleaned_data['faculty']

            # Have to do a separate case for when it's a tmp file and when it's already in memory
            try:
                if courses and isinstance(courses, TemporaryUploadedFile):
                    courses = parseCoursesFromPath(courses.temporary_file_path())
                elif courses and isinstance(courses, InMemoryUploadedFile):
                    f = TextIOWrapper(courses.file, encoding=request.encoding)
                    courses = parseCourses(f)
            except MissingHeaders as e:
                if len(e.headers) > 5:
                    errors.append("Missing too many headers in the schedule spreadsheet")
                else:
                    errors.append("Missing headers in the schedule spreadsheet: " + str(e.headers))

            try:
                if people and isinstance(people, TemporaryUploadedFile):
                    people = parsePeopleFromPath(people.temporary_file_path())
                elif people and isinstance(people, InMemoryUploadedFile):
                    f = TextIOWrapper(people.file, encoding=request.encoding)
                    people = parsePeople(f)
            except MissingHeaders as e:
                if len(e.headers) > 5:
                    errors.append("Missing too many TA preferences in the TA preferences spreadsheet")
                else:
                    errors.append("Missing headers in the TA preferences spreadsheet: " + str(e.headers))

            try:
                if faculty and isinstance(faculty, TemporaryUploadedFile):
                    faculty = parseFacultyHoursFromPath(faculty.temporary_file_path())
                elif faculty and isinstance(faculty, InMemoryUploadedFile):
                    f = TextIOWrapper(faculty.file, encoding=request.encoding)
                    faculty = parseFacultyHours(f)
            except MissingHeaders as e:
                if len(e.headers) > 5:
                    errors.append("Missing too many headers in the faculty hours spreadsheet")
                else:
                    errors.append("Missing headers in the faculty hours spreadsheet: " + str(e.headers))
        else:
            errors.append("Invalid form submission")
            print(form.errors)

        # Check if there were any parsing errors
        if len(errors) > 0:
            return JsonResponse({"errors": errors})
        else:
            generate(courses, people, faculty)
            return HttpResponse("generated a schedule")
    raise Http404()
