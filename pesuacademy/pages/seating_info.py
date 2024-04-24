import datetime

import requests_html
from bs4 import BeautifulSoup

from pesuacademy import util
from pesuacademy.models import SeatingInfo

# https://www.pesuacademy.com/Academy/s/studentProfilePESUAdmin?menuId=655&url=studentProfilePESUAdmin&controllerMode=6404&actionType=5&id=0&selectedData=0&_=1713930380582
class SeatingInfoHandler:
    @staticmethod
    def get_page(session: requests_html.HTMLSession) -> list[SeatingInfo]:
        try:
            profile_url = (
                "https://www.pesuacademy.com/Academy/s/studentProfilePESUAdmin"
            )
            query = {
                "menuId": "655",
                "url": "studentProfilePESUAdmin",
                "controllerMode": "6404",
                "actionType": "5",
                "id": "0",
                "selectedData": "0",
                "_": str(int(datetime.datetime.now().timestamp() * 1000)),
            }
            response = session.get(profile_url, allow_redirects=False, params=query)
            if response.status_code != 200:
                raise ConnectionError("Unable to fetch seating info.")
            soup = BeautifulSoup(response.text, "lxml")
            return util.seating_info.get_seating_info_from_page(soup)
        except Exception:
            raise ConnectionError("Unable to fetch seating info.")
