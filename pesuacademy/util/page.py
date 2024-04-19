import datetime
from typing import Optional

import requests_html
from bs4 import BeautifulSoup

from pesuacademy import pages


class PageHandler:
    def __init__(self, session: requests_html.HTMLSession):
        self.__session = session
        self._semester_ids = dict()
        self.course_page_handler = pages.CoursesPageHandler()
        self.attendance_page_handler = pages.AttendancePageHandler()
        self.profile_page_handler = pages.ProfilePageHandler()

    def set_semester_id_to_number_mapping(self, csrf_token: str):
        try:
            url = "https://www.pesuacademy.com/Academy/a/studentProfilePESU/getStudentSemestersPESU"
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
                "x-requested-with": "XMLHttpRequest",
            }
            response = self.__session.get(
                url, allow_redirects=False, params=query, headers=headers
            )
            if response.status_code != 200:
                raise ConnectionError("Unable to fetch course data.")
        except Exception:
            raise ConnectionError("Unable to fetch course data.")

        option_tags = response.json()
        option_tags = BeautifulSoup(option_tags, "lxml")
        option_tags = option_tags.find_all("option")
        semester_string_ids = list(map(lambda x: x.attrs["value"], option_tags))
        # TODO: Handle CIE semesters (sometimes the tag is <option value="972">CIE - Level2 (Odd Sem)</option>
        semester_numbers = list(
            map(lambda x: int(x.text.split("Sem-")[1]), option_tags)
        )
        semesters = dict(zip(semester_numbers, semester_string_ids))
        self._semester_ids = semesters

    def get_semester_ids_from_semester_number(
            self, semester: Optional[int] = None
    ) -> dict:
        """
        Get the semester ids from the semester number. If semester is not provided, all semester ids are returned.
        :param semester: The semester number.
        :return: The semester ids mapping.
        """
        assert (
                semester is None or 1 <= semester <= 8
        ), "Semester number should be between 1 and 8."
        return (
            self._semester_ids
            if semester is None
            else {semester: self._semester_ids[semester]}
        )

    def get_profile(self):
        return self.profile_page_handler.get_page(self.__session)

    def get_courses(self, semester: Optional[int] = None):
        semester_ids = self.get_semester_ids_from_semester_number(semester)
        return self.course_page_handler.get_page(self.__session, semester_ids)

    def get_attendance(self, semester: Optional[int] = None):
        semester_ids = self.get_semester_ids_from_semester_number(semester)
        return self.attendance_page_handler.get_page(self.__session, semester_ids)
