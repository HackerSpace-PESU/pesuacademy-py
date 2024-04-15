import datetime

import requests_html
from bs4 import BeautifulSoup

from pesu_academy.models import Profile


def get_profile_page(session: requests_html.HTMLSession) -> Profile:
    try:
        profile_url = "https://www.pesuacademy.com/Academy/s/studentProfilePESUAdmin"
        query = {
            "menuId": "670",
            "url": "studentProfilePESUAdmin",
            "controllerMode": "6414",
            "actionType": "5",
            "id": "0",
            "selectedData": "0",
            "_": str(int(datetime.datetime.now().timestamp() * 1000)),
        }
        response = session.get(profile_url, allow_redirects=False, params=query)
        if response.status_code != 200:
            raise ConnectionError("Unable to fetch profile data.")
        soup = BeautifulSoup(response.text, "lxml")
    except Exception:
        raise ConnectionError("Unable to fetch profile data.")

    profile = Profile()
    for element in soup.find_all("div", attrs={"class": "form-group"}):
        key = element.find("label",
                           attrs={"class": "col-md-12 col-xs-12 control-label lbl-title-light text-left"})
        if key is None:
            continue
        else:
            key = key.text.strip()
        if element.text.strip() in ["Email ID", "Contact No", "Aadhar No", "Name as in aadhar"]:
            value_tag = "input"
            value_class_name = "form-control"
            value = element.find(value_tag, attrs={"class": value_class_name}).attrs["value"].strip()
        else:
            value_tag = "label"
            value_class_name = "col-md-12 col-xs-12 control-label text-left"
            value = element.find(value_tag, attrs={"class": value_class_name}).text.strip()
        # TODO: Convert DOB to datetime
        # TODO: Convert numbers to floats/integers
        setattr(profile, key, value)
    return profile
