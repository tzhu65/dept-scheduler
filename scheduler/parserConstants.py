"""Constants for parsing from the csv files."""


class ParserPreferencesHeaders:
    """Headers for the preferences csv file."""
    ASSISTING_PREF = "Your preference for assisting."
    CATEGORY_ASSISTING = "If you could choose between teaching, recitation, assisting, and Math Help Center, " + \
                         "which would you want most? [Assiting]"
    CATEGORY_LABS = "If you could choose between teaching, recitation, assisting, and Math Help Center, " + \
                    "which would you want most? [Labs]"
    CATEGORY_MHC = "If you could choose between teaching, recitation, assisting, and Math Help Center, " + \
                   "which would you want most? [Math help center]"
    CATEGORY_RECITATION = "If you could choose between teaching, recitation, assisting, and Math Help Center, " + \
                          "which would you want most? [Recitation]"
    CATEGORY_TEACHING = "If you could choose between teaching, recitation, assisting, and Math Help Center, " + \
                        "which would you want most? [Teaching]"
    COMPUTER_SKILLS = "Your computer programming skills?"
    DAY_PREF = "Your day preference."
    FULLY_SUPPORTED = "Do you expect to be fully supported as a research assistant " + \
                      "for the entire academic year next year?"
    HOURS_BOUGHT_OUT = "Based on the above description of TA hours and assignments, " + \
                       "how many hours, if any, do you expect to be BOUGHT OUT of?"
    HOURS_COMPLETED = "Hours completed last semester (0 for fall)"
    LAB_PREF = "Your preference for labs."
    NAME = "Name"
    PURE_OR_APPLIED = "Pure or Applied?"
    QUALIFYING_EXAMS = "Qualifying exams passed to date?"
    RECITATION_PREF = "Your recitation preference."
    RETURNING = "Will you be returning in Fall?"
    SUPPORTING_PROFESSOR = "If you will be bought out of any Fall hours, " + \
                           "what is the name of the professor who will be supporting you?"
    TEACHING_PREF = "Your preference for teaching."
    TIME_CONFLICT = "Your time conflicts. Which of these classes will you take in Fall 2018?"
    YEAR_IN_SCHOOL = "What year will you be in Fall?"   # TODO: handle Spring case? Regex?


class ParserScheduleHeaders:
    """Headers for the schedule csv file."""
    ASSIST_COUNT = "Assist(6)"
    ASSISTING_ASSIGNMENT = "Assisting Assignment"
    BUILDING = "Bldg"
    CLASS = "Class"
    CLASS_NUMBER = "Class #"
    DAYS = "Days"
    END_TIME = "End Time"
    ENROLL_CAP = "Enroll Cap"
    INSTRUCTOR = "Instructor"
    LAB_COUNT = "Lab(6)"
    RECITATION_COUNT = "Recitation(3)"
    ROOM = "Rm"
    ROOM_CAP = "Rm Cap"
    SECTION = "Sec"
    START_TIME = "Start Time"
    TEACH_COUNT = "Teach(12)"


class ParserFacultyHoursHeaders:
    """Headers for the faculty hours csv file."""
    FALL = "Fall"
    PROFESSOR_NAME = "Professor Name"
    SPRING = "Spring"


class ParserConstants:
    """Constants for parsing responses."""
    COMPUTER_SKILLS = {"weak": 1, "ok": 2, "strong": 3}
    COMPUTER_SKILLS_NONE = 0

    POSITION_TEACH = "teach"
    POSITION_RECITATION = "recitation"
    POSITION_ASSIST = "assist"
    POSITION_LAB = "lab"

    CATEGORY_PREFS_LABS = "Labs"
    CATEGORY_PREFS_TEACHING = "Teaching"
    CATEGORY_PREFS_ASSISTING = "Assisting"
    CATEGORY_PREFS_RECITATION = "Recitation"
    CATEGORY_PREFS_MHC = "MHC"

    NO = "No"
    YES = "Yes"
