import datetime
import re

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests_html
from bs4 import BeautifulSoup

from pesuacademy.models.announcement import Announcement, AnnouncementFile


class AnnouncementPageHandler:
    @staticmethod
    def get_announcement_by_id(
        session: requests_html.HTMLSession, csrf_token: str, announcement_id: str
    ) -> Announcement:
        url = "https://www.pesuacademy.com/Academy/s/studentProfilePESUAdmin"
        data = {
            "controllerMode": "6411",
            "actionType": "4",
            "AnnouncementId": announcement_id,
            "menuId": "667",
        }
        headers = {
            "accept": "*/*",
            "accept-language": "en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.pesuacademy.com",
            "priority": "u=1, i",
            "referer": "https://www.pesuacademy.com/Academy/s/studentProfilePESU",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "x-csrf-token": csrf_token,
            "x-requested-with": "XMLHttpRequest",
        }

        response = session.post(url, data=data, headers=headers)
        if response.status_code != 200:
            data["actionType"] = "6"
            response = session.post(url, data=data, headers=headers)

        soup = BeautifulSoup(response.text, "lxml")

        title = soup.find("h4", class_="text-info").text.strip()
        date = soup.find("span", class_="text-muted text-date pull-right").text.strip()
        date = datetime.datetime.strptime(date, "%d-%B-%Y").date()

        content_tag = soup.find("div", class_="col-md-12")
        if content_tag is None:
            content_tag = soup.find("div", class_="col-md-8")
        paragraph_or_list_tags = content_tag.find_all(["p", "li"])
        content = "\n".join([tag.text.strip() for tag in paragraph_or_list_tags])

        img_tag = soup.find("img", class_="img-responsive")
        img = img_tag.attrs["src"] if img_tag else None

        attachment_tags = [
            tag
            for tag in content_tag.find_all("a")
            if tag.text.strip().endswith(".pdf")
        ]
        attachments = list()
        for attachment_tag in attachment_tags:
            attachment_name = attachment_tag.text.strip()
            pattern = re.compile(r"handleDownloadAnoncemntdoc\('(\d+)'\)")
            attachment_id = re.findall(pattern, attachment_tag.attrs["href"])[0]
            response = session.get(
                f"https://pesuacademy.com/Academy/s/studentProfilePESUAdmin/downloadAnoncemntdoc/{attachment_id}",
                headers={"x-csrf-token": csrf_token},
                verify=False,
            )
            attachment_bytes = response.content
            attachments.append(
                AnnouncementFile(name=attachment_name, content=attachment_bytes)
            )

        return Announcement(
            title=title, date=date, content=content, img=img, files=attachments
        )

    def get_page(
        self, session: requests_html.HTMLSession, csrf_token: str
    ) -> list[Announcement]:
        url = "https://www.pesuacademy.com/Academy/s/studentProfilePESUAdmin"
        query = {
            "menuId": "667",
            "controllerMode": "6411",
            "actionType": "5",
            "_": str(int(datetime.datetime.now().timestamp() * 1000)),
        }
        response = session.get(url, allow_redirects=False, params=query)
        if response.status_code != 200:
            raise ConnectionError("Unable to fetch announcement data.")
        soup = BeautifulSoup(response.text, "lxml")

        announcement_ids = soup.find_all("a", class_="pull-right readmorelink")
        pattern = re.compile(r"handleShowMoreAnnouncement\(\d+, \d+,(\d+)\)")
        announcement_ids = [
            pattern.match(ann.attrs.get("onclick")).group(1) for ann in announcement_ids
        ]

        announcements = list()
        for announcement_id in announcement_ids:
            announcements.append(
                self.get_announcement_by_id(session, csrf_token, announcement_id)
            )
        return announcements
