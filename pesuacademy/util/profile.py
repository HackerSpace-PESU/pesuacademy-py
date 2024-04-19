from bs4 import BeautifulSoup
import datetime
from pesuacademy.models import (
    ClassAndSectionInfo,
    Profile,
    PersonalDetails,
    OtherInformation,
    QualifyingExamination,
    ParentDetails,
    AddressDetails
)


def create_class_and_section_object_from_know_your_class_and_section(soup: BeautifulSoup) -> ClassAndSectionInfo:
    """
    Create a ClassAndSectionInfo object from the Know Your Class and Section page.
    :param soup: The BeautifulSoup object of the page.
    :return: The ClassAndSectionInfo object.
    """
    profile_data = dict()
    for th, td in zip(soup.find_all("th"), soup.find_all("td")):
        key = th.text.strip().lower()
        value = td.text.strip()
        value = None if value == "NA" else value
        if key == "class":
            key = "semester"
        elif key == "institute name":
            key = "institute"
        profile_data[key] = value
    return ClassAndSectionInfo(**profile_data)

def create_profile_object_from_profile_page(soup: BeautifulSoup) -> Profile:
    """
    Create a Profile object from the Profile page.
    :param soup: The BeautifulSoup object of the page.
    :return: The Profile object.
    """
    profile_data = dict()
    for element in soup.find_all("div", attrs={"class": "form-group"}):
        key = element.find("label",
                           attrs={"class": "col-md-12 col-xs-12 control-label lbl-title-light text-left"})
        if key is None:
            continue
        else:
            key = key.text.strip().lower().replace(" ", "_")



        if element.text.strip() in ["Email ID", "Contact No", "Aadhar No", "Name as in aadhar"]:
            value_tag = "input"
            value_class_name = "form-control"
            value = element.find(value_tag, attrs={"class": value_class_name}).attrs["value"].strip()
        else:
            value_tag = "label"
            value_class_name = "col-md-12 col-xs-12 control-label text-left"
            value = element.find(value_tag, attrs={"class": value_class_name}).text.strip()

        value = None if value == "NA" else value
        profile_data[key] = value

    personal_details = PersonalDetails(
        name=profile_data["name"],
        prn=profile_data["pesu_id"],
        srn=profile_data["srn"],
        program=profile_data["program"],
        branch=profile_data["branch"],
        semester=profile_data["semester"],
        section=profile_data["section"],
        email=profile_data["email_id"],
        mobile=profile_data["contact_no"],
        aadhar=profile_data["aadhar_no"],
        name_as_in_aadhar=profile_data["name_as_in_aadhar"]
    )

    other_information = OtherInformation(
        sslc=float(profile_data["sslc_marks"]),
        puc=float(profile_data["puc_marks"]),
        dob=datetime.datetime.strptime(profile_data["date_of_birth"], "%d- %m- %Y").date(),
        blood_group=profile_data["blood_group"]
    )

    qualifying_examination = QualifyingExamination(
        exam=profile_data["exam"],
        rank=int(profile_data["rank"]),
        score=float(profile_data["score"]) if profile_data["score"] is not None else None
    )

    mother_details = ParentDetails(
        name=profile_data["mother_name"],
        occupation=profile_data["mother_occupation"],
        email=profile_data["mother_email"],
        mobile=profile_data["mother_contact_no"]

    )

    return Profile(
        personal_details=personal_details,
        other_information=other_information,
        qualifying_examination=qualifying_examination
    )
