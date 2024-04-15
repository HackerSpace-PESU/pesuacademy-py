import datetime
from typing import Optional

import requests_html
from bs4 import BeautifulSoup

from pesu_academy.models import Course


def get_courses_in_semester(session: requests_html.HTMLSession, semester_value: Optional[int] = None):
    try:
        url = "https://www.pesuacademy.com/Academy/s/studentProfilePESUAdmin"
        query = {
            "menuId": "653",
            "controllerMode": "6403",
            "actionType": "38",
            "id": f"{semester_value}",
            "_": str(int(datetime.datetime.now().timestamp() * 1000)),
        }
        response = session.get(url, allow_redirects=False, params=query)
        if response.status_code != 200:
            raise ConnectionError("Unable to fetch profile data.")
        soup = BeautifulSoup(response.text, "lxml")
    except Exception:
        raise ConnectionError("Unable to fetch profile data.")

    courses = []
    table = soup.find("table", attrs={"class": "table table-hover box-shadow"})
    table_body = table.find("tbody")
    for row in table_body.find_all("tr"):
        columns = row.find_all("td")
        if len(columns) == 1 and columns[0].text.strip() == 'No\n\t\t\t\t\t\tsubjects found':
            break
        course_code = columns[0].text.strip()
        course_title = columns[1].text.strip()
        course_type = columns[2].text.strip()
        course_status = columns[3].text.strip()
        course = Course(course_code, course_title, course_type, course_status)
        courses.append(course)
    return courses


def get_courses_page(session: requests_html.HTMLSession, csrf_token: str, semester: Optional[int] = None) -> dict[
    int, list[Course]]:
    try:
        profile_url = "https://www.pesuacademy.com/Academy/a/studentProfilePESU/getStudentSemestersPESU"
        query = {"_": str(int(datetime.datetime.now().timestamp() * 1000))}
        headers = {
            "accept": "*/*",
            "accept-language": "en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded",
            "referer": "https://www.pesuacademy.com/Academy/s/studentProfilePESU",
            "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "x-csrf-token": csrf_token,
            "x-requested-with": "XMLHttpRequest"
        }
        response = session.get(profile_url, allow_redirects=False, params=query, headers=headers)
        if response.status_code != 200:
            raise ConnectionError("Unable to fetch course data.")
    except Exception:
        raise ConnectionError("Unable to fetch course data.")

    option_tags = response.json()
    option_tags = BeautifulSoup(option_tags, "lxml")
    option_tags = option_tags.find_all("option")
    courses = dict()
    for semester_option_tag in option_tags:
        current_value = semester_option_tag.attrs["value"]
        current_semester = int(semester_option_tag.text.split("Sem-")[1])
        if semester is None or current_semester == semester:
            courses_in_semester = get_courses_in_semester(session, current_value)
            courses[current_semester] = courses_in_semester

    courses = dict(sorted(courses.items()))
    return courses
