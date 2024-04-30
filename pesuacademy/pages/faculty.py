from bs4 import BeautifulSoup
import requests_html
from typing import Optional
from pesuacademy.models.professor import Professor


class FacultyPageHandler:
    departments = {
        "arch": "architecture",
        "bt": "biotechnology",
        "cv": "civil",
        "cse": "computer-science",
        "cse-aiml": "computer-science-AIML",
        "ca": "computer-application",
        "des": "design",
        "eee": "electrical-&-electronics",
        "ece": "electronics-&-communications",
        "law": "law",
        "me": "mechanical",
        "ms": "management-studies",
        "sh": "science-&-humanities",
        "com": "commerce",
        "psy": "psychology",
        "cie": "centre-for-innovation-&-entrepreneurship",
        "ps": "pharmaceutical-sciences",
    }
    campuses = ["rr", "ec", "hn"]

    @staticmethod
    def get_urls_from_campus_and_department(
        campus: Optional[str], department: Optional[str]
    ):
        base_url = "https://staff.pes.edu/{campus}/atoz/{department}"
        if department:
            assert (
                department in FacultyPageHandler.departments
            ), "Invalid department provided."
        if campus:
            assert campus in FacultyPageHandler.campuses, "Invalid campus provided."

        if not department and not campus:
            urls = [base_url.format(campus="", department="")]
        elif department and not campus:
            urls = [
                base_url.format(
                    campus=campus, department=FacultyPageHandler.departments[department]
                )
                for campus in ["rr", "ec", "hn"]
            ]
        elif campus and not department:
            urls = [
                base_url.format(
                    campus=campus, department=FacultyPageHandler.departments[department]
                )
                for department in FacultyPageHandler.departments
            ]
        else:
            urls = [
                base_url.format(
                    campus=campus, department=FacultyPageHandler.departments[department]
                )
            ]
        return urls

    @staticmethod
    def get_staff_details() -> list[Professor]:
        try:
            base_url = "https://staff.pes.edu/atoz/"
            session = HTMLSession()
            response = session.get(base_url)
            if response.status_code != 200:
                raise ConnectionError(f"Failed to fetch URL: {base_url}")

            soup = BeautifulSoup(response.text, "html.parser")
            last_page_span = soup.find(
                "span", {"aria-hidden": "true"}
            )  # getting the last page from the pagination end
            last_page_number = int(last_page_span.get_text())
            PESU_STAFF_LIST = []
            for page_num in range(1, last_page_number + 1):
                print("Scraping page:", page_num)
                staff_url = f"{base_url}?page={page_num}"
                response = session.get(staff_url)
                soup = BeautifulSoup(response.text, "html.parser")

                staff_divs = soup.find_all("div", class_="staff-profile")
                for staff_div in staff_divs:
                    anchor_tag = staff_div.find("a", class_="geodir-category-img_item")
                    if anchor_tag:
                        base_url_single_staff = "https://staff.pes.edu/"
                        staff_url = anchor_tag["href"]
                        request_path = base_url_single_staff + staff_url[1:]
                        PESU_STAFF = StaffPageHandler.get_details_from_url(
                            request_path, session
                        )
                        PESU_STAFF_LIST.append(PESU_STAFF)

            return PESU_STAFF_LIST

        except Exception as e:
            print(f"Error occurred: {e}")
            raise ConnectionError("Unable to fetch staff data.")
        finally:
            session.close()

    @staticmethod
    def get_details_from_url(url, session):
        response = session.get(url)
        if response.status_code != 200:
            raise ConnectionError(f"Failed to fetch URL: {url}")
        soup = BeautifulSoup(response.text, "html.parser")
        # name
        name_tag = soup.find("h4")
        name = name_tag.text.strip() if name_tag else None
        # domain
        teaching_items = soup.select(
            "#tab-teaching .bookings-item-content ul.ul-item-left li"
        )
        domains = [item.text.strip() for item in teaching_items]
        # designation
        designation = soup.find("h5")
        designation = " ".join(designation.text.split())
        # Education
        professor_education = []
        education_section = soup.find_all("h3")
        education_section_filter = [
            h3 for h3 in education_section if h3.get_text(strip=True) == "Education"
        ]

        for h3 in education_section_filter:
            education_list = h3.find_next("ul", class_="ul-item-left")
            if education_list:
                education_items = education_list.find_all("li")
                education_details = [
                    item.find("p").text.strip() for item in education_items
                ]
                for detail in education_details:
                    professor_education.append(detail)

        # print(professor_education)

        # Experience
        professor_experience = []
        experience_section = soup.find_all("h3")
        experience_section_filter = [
            h3 for h3 in experience_section if h3.get_text(strip=True) == "Experience"
        ]
        for h3 in experience_section_filter:
            experience_list = h3.find_next("ul", class_="ul-item-left")
            if experience_list:
                experience_items = experience_list.find_all("li")
                experience_details = [
                    item.find("p").text.strip() for item in experience_items
                ]
                for detail in experience_details:
                    professor_experience.append(detail)

        # print(professor_experience)

        # email
        all_a_tags = soup.find_all("a")
        email = [
            tag
            for tag in all_a_tags
            if "pes.edu" in tag.get("href", "") and "pes.edu" in tag.get_text()
        ]
        if email:
            email = email[0].get_text()
        # department
        department_element = soup.find("li", class_="contat-card")
        department_paragraph = department_element.find("p")
        department = department_paragraph.get_text(strip=True)
        # campus
        try:
            campus_element = soup.find_all("li", class_="contat-card")[1]
            if campus_element:
                campus_paragraph = campus_element.find("p")
                campus = campus_paragraph.get_text(strip=True)
        except IndexError:
            campus = None
        # responsibilities
        responsibilities = []
        responsibilities_div = soup.find("div", id="tab-responsibilities")
        if responsibilities_div is not None:
            p_tags = responsibilities_div.find_all("p")
            responsibilities = [p.text for p in p_tags]
        Pesu_Staff = Professor(
            name=name,
            designation=designation,
            education=professor_education,
            experience=professor_experience,
            department=department,
            campus=campus,
            domains=domains,
            email=email,
            responsibilities=responsibilities,
        )
        return Pesu_Staff

    def get_page(
        self,
        session: requests_html.HTMLSession,
        campus: Optional[str] = None,
        department: Optional[str] = None,
        designation: Optional[str] = None,
    ) -> list[Professor]:
        urls = self.get_urls_from_campus_and_department(campus, department)
        # TODO: Scrape the data from the URLs. Use the same session object provided.
        # professors = list()
        # for url in urls:
        #     professors.extend(get_faculty(session, url))
        # return professors
