import datetime

from bs4 import BeautifulSoup

from pesuacademy.models import (
    ClassAndSectionInfo,
    Profile,
    PersonalDetails,
    OtherInformation,
    QualifyingExamination,
    ParentDetails,
    ParentInformation,
    AddressDetails,
)


def get_data_from_section(soup: BeautifulSoup) -> dict:
    """
    Get the data from a row in the Profile page.
    :param soup: The BeautifulSoup object of the row.
    :return: The data in the row.
    """
    data = dict()
    for element in soup.find_all("div", attrs={"class": "form-group"}):
        key = element.find(
            "label",
            attrs={
                "class": "col-md-12 col-xs-12 control-label lbl-title-light text-left"
            },
        )
        if key is None:
            continue
        else:
            key = key.text.strip().lower().replace(" ", "_")

        value_tag = "label"
        value_class_name = "col-md-12 col-xs-12 control-label text-left"
        value = element.find(value_tag, attrs={"class": value_class_name}).text.strip()
        value = None if value == "NA" else value
        data[key] = value
    return data


def create_class_and_section_object_from_know_your_class_and_section(
    soup: BeautifulSoup,
) -> ClassAndSectionInfo:
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


def create_personal_details_object_from_profile_page(
    soup: BeautifulSoup,
) -> PersonalDetails:
    """
    Create a PersonalDetails object from the Profile page.
    :param soup: The BeautifulSoup object of the page.
    :return: The PersonalDetails object.
    """

    personal_details = dict()
    personal_details_section = soup.find(
        "div", attrs={"class": "elem-info-wrapper box-shadow clearfix"}
    )
    for element in personal_details_section.find_all(
        "div", attrs={"class": "form-group"}
    ):
        key = element.find(
            "label",
            attrs={
                "class": "col-md-12 col-xs-12 control-label lbl-title-light text-left"
            },
        )
        if key is None:
            continue
        else:
            key = key.text.strip().lower().replace(" ", "_")

        if element.text.strip() in [
            "Email ID",
            "Contact No",
            "Aadhar No",
            "Name as in aadhar",
        ]:
            value_tag = "input"
            value_class_name = "form-control"
            value = (
                element.find(value_tag, attrs={"class": value_class_name})
                .attrs["value"]
                .strip()
            )
        else:
            value_tag = "label"
            value_class_name = "col-md-12 col-xs-12 control-label text-left"
            value = element.find(
                value_tag, attrs={"class": value_class_name}
            ).text.strip()

        value = None if value == "NA" else value
        personal_details[key] = value

    image_b64_encoded = soup.find("img", attrs={"class": "media-object"})["src"]

    return PersonalDetails(
        name=personal_details["name"],
        prn=personal_details["pesu_id"],
        srn=personal_details["srn"],
        program=personal_details["program"],
        branch=personal_details["branch"],
        semester=personal_details["semester"],
        section=personal_details["section"],
        img=image_b64_encoded,
        email=personal_details["email_id"],
        mobile=personal_details["contact_no"],
        aadhar=personal_details["aadhar_no"],
        name_as_in_aadhar=personal_details["name_as_in_aadhar"],
    )


def create_other_information_object_from_profile_page(
    soup: BeautifulSoup,
) -> OtherInformation:
    """
    Create an OtherInformation object from the Profile page.
    :param soup: The BeautifulSoup object of the page.
    :return: The OtherInformation object.
    """
    other_information_section = soup.find_all(
        "div", attrs={"class": "dashboard-info-bar box-shadow"}
    )[0]
    other_information = get_data_from_section(other_information_section)
    return OtherInformation(
        sslc=float(other_information["sslc_marks"]),
        puc=float(other_information["puc_marks"]),
        dob=datetime.datetime.strptime(
            other_information["date_of_birth"], "%d- %m- %Y"
        ).date(),
        blood_group=other_information["blood_group"],
    )


def create_qualifying_examination_object_from_profile_page(
    soup: BeautifulSoup,
) -> QualifyingExamination:
    """
    Create a QualifyingExamination object from the Profile page.
    :param soup: The BeautifulSoup object of the page.
    :return: The QualifyingExamination object.
    """
    qualifying_examination_section = soup.find_all(
        "div", attrs={"class": "dashboard-info-bar box-shadow"}
    )[1]
    qualifying_examination = get_data_from_section(qualifying_examination_section)
    return QualifyingExamination(
        exam=qualifying_examination["exam"],
        rank=int(qualifying_examination["rank"]),
        score=(
            float(qualifying_examination["score"])
            if qualifying_examination["score"] is not None
            else None
        ),
    )


def create_parent_details_object_from_profile_page(
    soup: BeautifulSoup,
) -> ParentDetails:
    """
    Create a ParentDetails object from the Profile page.
    :param soup: The BeautifulSoup object of the page.
    :return: The ParentDetails object.
    """
    parent_details = {"mother": None, "father": None}
    parent_details_section = soup.find_all(
        "div", attrs={"class": "elem-info-wrapper box-shadow clearfix"}
    )[1]
    for parent_section in parent_details_section.find_all(
        "div", attrs={"class": "col-md-6"}
    ):
        parent_data = get_data_from_section(parent_section)
        parent_type = "mother" if "mother_name" in parent_data else "father"
        parent_details[parent_type] = ParentInformation(
            name=parent_data[f"{parent_type}_name"],
            mobile=parent_data["mobile"],
            email=parent_data["email"],
            occupation=parent_data["occupation"],
            qualification=parent_data["qualification"],
            designation=parent_data["designation"],
            employer=parent_data["employer"],
        )
    return ParentDetails(
        mother=parent_details["mother"], father=parent_details["father"]
    )


def create_address_details_object_from_profile_page(
    soup: BeautifulSoup,
) -> AddressDetails:
    """
    Create an AddressDetails object from the Profile page.
    :param soup: The BeautifulSoup object of the page.
    :return: The AddressDetails object.
    """
    address_details_section = soup.find_all(
        "div", attrs={"class": "dashboard-info-bar box-shadow"}
    )[2]
    address_details = get_data_from_section(address_details_section)
    return AddressDetails(
        present=address_details["present_address"],
        permanent=address_details["permanent_address"],
    )


def create_profile_object_from_profile_page(soup: BeautifulSoup) -> Profile:
    """
    Create a Profile object from the Profile page.
    :param soup: The BeautifulSoup object of the page.
    :return: The Profile object.
    """
    personal_details = create_personal_details_object_from_profile_page(soup)
    other_information = create_other_information_object_from_profile_page(soup)
    qualifying_examination = create_qualifying_examination_object_from_profile_page(
        soup
    )
    parent_details = create_parent_details_object_from_profile_page(soup)
    address_details = create_address_details_object_from_profile_page(soup)
    return Profile(
        personal_details=personal_details,
        other_information=other_information,
        qualifying_examination=qualifying_examination,
        parent_details=parent_details,
        address_details=address_details,
    )
