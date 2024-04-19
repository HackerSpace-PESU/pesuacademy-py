import datetime
from typing import Optional

import requests_html
from bs4 import BeautifulSoup

from pesuacademy.models import Course, Attendance


class AttendancePageHandler:
    @staticmethod
    def get_attendance_in_semester(
            session: requests_html.HTMLSession, semester_value: Optional[int] = None
    ):
        try:
            url = "https://www.pesuacademy.com/Academy/s/studentProfilePESUAdmin"
            query = {
                "menuId": "660",
                "controllerMode": "6407",
                "actionType": "8",
                "batchClassId": f"{semester_value}",
                "_": str(int(datetime.datetime.now().timestamp() * 1000)),
            }
            response = session.get(url, allow_redirects=False, params=query)
            if response.status_code != 200:
                raise ConnectionError("Unable to fetch attendance data.")
            soup = BeautifulSoup(response.text, "lxml")
        except Exception:
            raise ConnectionError("Unable to fetch profile data.")

        attendance = []
        table = soup.find("table", attrs={"class": "table box-shadow"})
        table_body = table.find("tbody")
        for row in table_body.find_all("tr"):
            columns = row.find_all("td")
            if (
                    len(columns) == 1
                    and columns[0].text.strip() == "Data Not\n\t\t\t\t\tAvailable"
            ):
                break
            course_code = columns[0].text.strip()
            course_title = columns[1].text.strip()
            attended_and_total_classes = columns[2].text.strip()
            if "/" in attended_and_total_classes:
                attended_classes, total_classes = list(
                    map(int, attended_and_total_classes.split("/"))
                )
            else:
                attended_classes, total_classes = None, None
            percentage = columns[3].text.strip()
            percentage = float(percentage) if percentage != "NA" else None
            course = Course(
                course_code,
                course_title,
                attendance=Attendance(attended_classes, total_classes, percentage),
            )
            attendance.append(course)
        return attendance

    @staticmethod
    def get_page(
            session: requests_html.HTMLSession, semester_ids: dict
    ) -> dict[int, list[Course]]:
        attendance = dict()
        for semester_number in semester_ids:
            attendance_in_semester = AttendancePageHandler.get_attendance_in_semester(
                session, semester_ids[semester_number]
            )
            attendance[semester_number] = attendance_in_semester
        attendance = dict(sorted(attendance.items()))
        return attendance
