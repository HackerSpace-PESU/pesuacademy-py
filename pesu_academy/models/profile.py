# TODO: Add a list of fields and assign them only. Do not allow any other fields to be added.
# TODO: Make separate profile for KYCAS and Profile
class Profile:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        return f"{self.__dict__}"
