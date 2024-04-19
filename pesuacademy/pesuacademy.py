from typing import Optional

import requests_html
from bs4 import BeautifulSoup

from .exceptions import CSRFTokenError, AuthenticationError
from .models import Profile, Course
from .pages import profile, courses, attendance, utils


class PESUAcademy:
    """
    A class to interact with PESU Academy website.
    This class is the entrypoint to all the functionality in this module
    """

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize the PESU Academy object.

        :param username: Your SRN, PRN or email address.
        :param password: Your password.
        """
        self.__session = requests_html.HTMLSession()
        self._authenticated: bool = False
        self._semester_ids = dict()
        self._csrf_token: str = self.generate_csrf_token(username, password)

    @property
    def authenticated(self):
        return self._authenticated

    def get_semester_ids_from_semester_number(self, semester: Optional[int] = None) -> dict:
        """
        Get the semester ids from the semester number. If semester is not provided, all semester ids are returned.

        :param semester: The semester number.
        :return: A Dictionary containing the mapping from the semester to the semester ID
        """
        assert semester is None or 1 <= semester <= 8, "Semester number should be between 1 and 8."
        return self._semester_ids if semester is None else {semester: self._semester_ids[semester]}

    def generate_csrf_token(self, username: Optional[str] = None, password: Optional[str] = None) -> str:
        """
        Generate a CSRF token. If username and password are provided, authenticate and get the CSRF token.

        :return: The CSRF token.
        """
        try:
            # Get the initial csrf token
            home_url = "https://www.pesuacademy.com/Academy/"
            response = self.__session.get(home_url)
            soup = BeautifulSoup(response.text, "lxml")
            csrf_token = soup.find("meta", attrs={"name": "csrf-token"})["content"]
        except Exception:
            self.__session.close()
            raise CSRFTokenError("Unable to fetch default csrf token. Please try again later.")

        if username and password:
            # Prepare the login data for auth call
            data = {
                "_csrf": csrf_token,
                "j_username": username,
                "j_password": password,
            }
            try:
                auth_url = "https://www.pesuacademy.com/Academy/j_spring_security_check"
                response = self.__session.post(auth_url, data=data)
                soup = BeautifulSoup(response.text, "lxml")
            except Exception as e:
                self.__session.close()
                raise AuthenticationError("Unable to authenticate. Please check your credentials.")

            # if class login-form is present, login failed
            if soup.find("div", attrs={"class": "login-form"}):
                self.__session.close()
                raise AuthenticationError("Invalid username or password, or the user does not exist.")

            # if login is successful, update the CSRF token
            csrf_token = soup.find("meta", attrs={"name": "csrf-token"})["content"]
            self._authenticated = True
            self._semester_ids = utils.get_semester_list(self.__session, csrf_token)

        return csrf_token

    def know_your_class_and_section(self, username: str) -> Profile:
        """
        Get the publicly visible class and section information of a student from the Know Your Class and Section page.

        :param username: The SRN, PRN or email address of the student.
        :return: The profile information.
        """
        try:
            response = self.__session.post(
                "https://www.pesuacademy.com/Academy/getStudentClassInfo",
                headers={
                    "authority": "www.pesuacademy.com",
                    "accept": "*/*",
                    "accept-language": "en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7",
                    "content-type": "application/x-www-form-urlencoded",
                    "origin": "https://www.pesuacademy.com",
                    "referer": "https://www.pesuacademy.com/Academy/",
                    "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Linux"',
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "x-csrf-token": self._csrf_token,
                    "x-requested-with": "XMLHttpRequest"
                },
                data={
                    "loginId": username
                }
            )
        except Exception:
            raise ValueError("Unable to get profile from Know Your Class and Section.")

        soup = BeautifulSoup(response.text, "html.parser")
        profile = Profile()
        for th, td in zip(soup.find_all("th"), soup.find_all("td")):
            key = th.text.strip()
            value = td.text.strip()
            setattr(profile, key, value)

        return profile

    def profile(self) -> Profile:
        """
        Get the private profile information of the currently authenticated user.

        :return: The profile information.
        """
        if not self._authenticated:
            raise AuthenticationError("You need to authenticate first.")
        profile_info = profile.get_profile_page(self.__session)
        return profile_info

    def courses(self, semester: Optional[int] = None) -> dict[int, list[Course]]:
        """
        Get the courses of the currently authenticated user.

        :param semester: The semester number. If not provided, all courses across all semesters are returned.
        :return: The course information for the given semester.
        """
        if not self._authenticated:
            raise AuthenticationError("You need to authenticate first.")
        semester_ids = self.get_semester_ids_from_semester_number(semester)
        courses_info = courses.get_courses_page(self.__session, semester_ids)
        return courses_info

    def attendance(self, semester: Optional[int] = None) -> dict[int, list[Course]]:
        """
        Get the attendance in courses of the currently authenticated user.
        
        :param semester: The semester number. If not provided, attendance across all semesters are returned.
        :return: The attendance information for the given semester.
        """
        if not self._authenticated:
            raise AuthenticationError("You need to authenticate first.")
        semester_ids = self.get_semester_ids_from_semester_number(semester)
        attendance_info = attendance.get_attendance_page(self.__session, semester_ids)
        return attendance_info
