import datetime

import requests_html
from bs4 import BeautifulSoup

from pesuacademy.models import SeatingInformation


class SeatingInformationHandler:
    @staticmethod
    def get_seating_information_from_page(
        soup: BeautifulSoup,
    ) -> list[SeatingInformation]:
        info_table = soup.find("table", attrs={"id": "seatinginfo"})
        tablebody = info_table.find("tbody")
        tablerows = tablebody.find_all("tr")
        seating_info = list()
        for row in tablerows:
            columns = row.find_all("td")
            assn_name = columns[0].text.strip()
            course_code = columns[1].text.strip()
            date = columns[2].text.strip()
            time = columns[3].text.strip()
            terminal = columns[4].text.strip()
            block = columns[5].text.strip()
            seating_info.append(
                SeatingInformation(assn_name, course_code, date, time, terminal, block)
            )
        return seating_info

    @staticmethod
    def get_page(session: requests_html.HTMLSession) -> list[SeatingInformation]:
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
            if (
                (no_seating_tag := soup.find("h5")) is not None
                and no_seating_tag.text == "No Test Seating Info is available"
            ):
                return []
            else:
                return SeatingInformationHandler.get_seating_information_from_page(soup)
        except Exception:
            raise ConnectionError("Unable to fetch seating info.")
