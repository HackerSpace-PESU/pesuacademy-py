import datetime
from typing import Optional

import requests_html
from bs4 import BeautifulSoup

from pesuacademy.models import Course


class CoursesPageHandler:
    @staticmethod
    def get_courses_in_semester(
        session: requests_html.HTMLSession, semester_id: Optional[int] = None
    ):
        try:
            url = "https://www.pesuacademy.com/Academy/s/studentProfilePESUAdmin"
            query = {
                "menuId": "653",
                "controllerMode": "6403",
                "actionType": "38",
                "id": f"{semester_id}",
                "_": str(int(datetime.datetime.now().timestamp() * 1000)),
            }
            response = session.get(url, allow_redirects=False, params=query)
            if response.status_code != 200:
                raise ConnectionError("Unable to fetch profile data.")
            soup = BeautifulSoup(response.text, "lxml")
        except Exception:
            raise ConnectionError("Unable to fetch courses data.")

        courses = []
        table = soup.find("table", attrs={"class": "table table-hover box-shadow"})
        table_body = table.find("tbody")
        for row in table_body.find_all("tr"):
            columns = row.find_all("td")
            if (
                len(columns) == 1
                and columns[0].text.strip() == "No\n\t\t\t\t\t\tsubjects found"
            ):
                break
            course_code = columns[0].text.strip()
            course_title = columns[1].text.strip()
            course_type = columns[2].text.strip()
            course_status = columns[3].text.strip()
            course = Course(course_code, course_title, course_type, course_status)
            courses.append(course)
        return courses

    @staticmethod
    def get_page(
        session: requests_html.HTMLSession, semester_ids: dict
    ) -> dict[int, list[Course]]:
        courses = dict()
        for semester_number in semester_ids:
            courses_in_semester = CoursesPageHandler.get_courses_in_semester(
                session, semester_ids[semester_number]
            )
            courses[semester_number] = courses_in_semester
        courses = dict(sorted(courses.items()))
        return courses
