from typing import Optional



class Staff:
    def __init__(
        self,
        name: str,
        designation: str,  
        campus: str,
        department: str,
        mail : str,
        domains: Optional[list]=None, 
        responsibilities: Optional[list]=None, 
        education:  Optional[list]=None,
        experience: Optional[list]=None,
    ):
        self.name = name
        self.designation = designation
        self.education = education
        self.experience = experience
        self.department = department
        self.campus = campus
        self.domains = domains
        self.mail = mail
        self.responsibilities = responsibilities

    def __str__(self):
        return f"{self.__dict__}"
