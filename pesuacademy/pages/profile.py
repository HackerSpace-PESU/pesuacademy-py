import datetime

import requests_html
from bs4 import BeautifulSoup

from pesuacademy import util
from pesuacademy.models import Profile


class ProfilePageHandler:
    @staticmethod
    def get_page(session: requests_html.HTMLSession) -> Profile:
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
            return util.profile.create_profile_object_from_profile_page(soup)
        except Exception:
            raise ConnectionError("Unable to fetch profile data.")
