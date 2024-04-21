class Staff:
    def __init__(
        self,
        name: str,
        designation: str,  
        education: list,
        experience: list,
        campus: str,
        department: str,
        domains: list,
        Responsibilities: list, 
        mail : str
    ):
        self.name = name
        self.designation = designation
        self.education = education
        self.experience = experience
        self.department = department
        self.campus = campus
        self.domains = domains
        self.Responsibilities = Responsibilities
        self.mail = mail

    def __str__(self):
        return f"{self.__dict__}"


