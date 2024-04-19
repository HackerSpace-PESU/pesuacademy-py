import datetime
from typing import Optional


class ClassAndSectionInfo:
    def __init__(
        self,
        prn: str,
        srn: str,
        name: str,
        semester: str,
        section: str,
        department: str,
        branch: str,
        institute: str,
        cycle: Optional[str] = None,
    ):
        self.prn = prn
        self.srn = srn
        self.name = name
        self.semester = semester
        self.section = section
        self.cycle = cycle
        self.department = department
        self.branch = branch
        self.institute = institute

    def __str__(self):
        return f"{self.__dict__}"


class PersonalDetails:
    def __init__(
        self,
        name: str,
        prn: str,
        srn: str,
        branch: str,
        semester: str,
        section: str,
        program: Optional[str] = None,
        email: Optional[str] = None,
        mobile: Optional[str] = None,
        aadhar: Optional[str] = None,
        name_as_in_aadhar: Optional[str] = None,
    ):
        self.name = name
        self.prn = prn
        self.srn = srn
        self.program = program
        self.branch = branch
        self.semester = semester
        self.section = section
        self.email = email
        self.mobile = mobile
        self.aadhar = aadhar
        self.name_as_in_aadhar = name_as_in_aadhar

    def __str__(self):
        return f"{self.__dict__}"


class OtherInformation:
    def __init__(self, sslc: float, puc: float, dob: datetime.date, blood_group: str):
        self.sslc = sslc
        self.puc = puc
        self.dob = dob
        self.blood_group = blood_group

    def __str__(self):
        return f"{self.__dict__}"


class QualifyingExamination:
    def __init__(self, exam: str, rank: int, score: float):
        self.exam = exam
        self.rank = rank
        self.score = score

    def __str__(self):
        return f"{self.__dict__}"


class ParentInformation:
    def __init__(
        self,
        name: str,
        mobile: str,
        email: str,
        occupation: str,
        qualification: str,
        designation: str,
        employer: str,
    ):
        self.name = name
        self.mobile = mobile
        self.email = email
        self.occupation = occupation
        self.qualification = qualification
        self.designation = designation
        self.employer = employer


class ParentDetails:
    def __init__(self, mother: ParentInformation, father: ParentInformation):
        self.mother = mother
        self.father = father

    def __str__(self):
        return f"{self.__dict__}"


def __str__(self):
    return f"{self.__dict__}"


class AddressDetails:
    def __init__(self, present: str, permanent: str):
        self.present = present
        self.permanent = permanent

    def __str__(self):
        return f"{self.__dict__}"


class Profile:
    def __init__(
        self,
        personal_details: PersonalDetails,
        other_information: OtherInformation,
        qualifying_examination: QualifyingExamination,
        parent_details: ParentDetails,
        address_details: AddressDetails,
    ):
        self.personal_details = personal_details
        self.other_information = other_information
        self.qualifying_examination = qualifying_examination
        self.parent_details = parent_details
        self.address_details = address_details

    def __str__(self):
        return f"{self.__dict__}"
