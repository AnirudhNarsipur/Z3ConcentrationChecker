from dataclasses import dataclass


@dataclass(frozen=True)
class StudentInfo:
    name : str
    student_email : str
    banner_id : str
    advisor_name : str
    advisor_email : str