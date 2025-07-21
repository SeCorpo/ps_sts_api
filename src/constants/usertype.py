import enum

class Usertype(enum.Enum):
    ADMIN_ORGANISATION = "admin_organisation"
    ADMIN_SCHOOL = "admin_school"
    TEACHER = "teacher"
    PARENT = "parent"
    STUDENT = "student"