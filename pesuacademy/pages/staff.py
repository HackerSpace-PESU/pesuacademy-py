import time
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup
from ..models.staff import Staff  

class StaffPageHandler:
    @staticmethod
    def get_staff_details() -> Staff:
        try:
            base_url = "https://staff.pes.edu/atoz/"
            session=HTMLSession()
            # options = Options()
            # options.add_argument("--disable-infobars")  
            # options.add_argument("--headless")
            # driver = webdriver.Chrome()  
            for page_num in range(1, 23):
                staff_url = f"{base_url}?page={page_num}"
                response = session.get(staff_url) 
                if response.status_code != 200:
                    raise ConnectionError(f"Failed to fetch URL: {staff_url}")
                soup=BeautifulSoup(response.text,"html.parser")    
                staff_divs = soup.find_all('div', class_='staff-profile')
                for staff_div in staff_divs:
                    anchor_tag = staff_div.find('a', class_='geodir-category-img_item')
                    if anchor_tag:
                        base_url_single_staff="https://staff.pes.edu/"
                        staff_url = anchor_tag['href']
                        request_path = base_url_single_staff + staff_url[1:]
                        # driver.get(request_path)
                        # time.sleep(3) 
                        # html = driver.page_source
                        # soup = BeautifulSoup(html, 'html.parser')
                        # StaffPageHandler.get_details_from_url(request_path, session)
                        PESU_STAFF=StaffPageHandler.get_details_from_url(request_path, session)
                        print(PESU_STAFF)
                        # return PESU_STAFF


        except Exception as e:
            print(f"Error occurred: {e}")
            raise ConnectionError("Unable to fetch staff data.")
        finally:
            session.close()
    @staticmethod
    def get_details_from_url(url, driver):
        # driver.get(url)
        # time.sleep(3) 

        # html = driver.page_source
        session=HTMLSession()
        response=session.get(url)
        if response.status_code != 200:
            raise ConnectionError(f"Failed to fetch URL: {url}")
        soup = BeautifulSoup(response.text, 'html.parser')
        #name
        name_tag = soup.find('h4')
        name = name_tag.text.strip() if name_tag else None
        #domain
        teaching_items = soup.select('#tab-teaching .bookings-item-content ul.ul-item-left li')
        domains = [item.text.strip() for item in teaching_items]
        #designation
        designation=soup.find('h5')
        designation = ' '.join(designation.text.split())
        #Education
        professor_education = []
        education_section = soup.find('h3', string='Education')
        if education_section:
            education_list = education_section.find_next('ul', class_='ul-item-left').find_all('li')
            education_details = [item.find('p').text.strip() for item in education_list]
            for detail in education_details:
                professor_education.append(detail)
            # print(professor_education)
            # print()
        #Experience
        professor_experience=[]
        experience_section = soup.find('h3', string='Experience')
        if experience_section:
            experience_list = experience_section.find_next('ul', class_='ul-item-left').find_all('li')
            experience_details = [item.find('p').text.strip() for item in experience_list]
            for detail in experience_details:
                professor_experience.append(detail)
            # print(professor_experience)
            # print()
        

        #email
        all_a_tags = soup.find_all("a")
        email = [
            tag for tag in all_a_tags
            if "pes.edu" in tag.get("href", "") and "pes.edu" in tag.get_text()
        ]
        email=email[0].get_text()

        #department
        department_element = soup.find('li', class_='contat-card')
        department_paragraph = department_element.find('p')
        department = department_paragraph.get_text(strip=True)

        #campus
        campus_element=soup.find_all('li', class_='contat-card')[1]
        campus_paragraph = campus_element.find('p')
        campus=campus_paragraph.get_text(strip=True)


        #responsibilities
        responsibilities=[]

        responsibilities_div = soup.find('div', id='tab-responsibilities')
        if(responsibilities_div is not None):
            # print(len(responsibilities_div))
            # print(responsibilities_div)
            p_tags = responsibilities_div.find_all('p')
            responsibilities = [p.text for p in p_tags]

        # print(responsibilities)
        # print()
        
        Pesu_Staff=Staff(name,designation,professor_education,professor_experience,campus,department,domains,responsibilities,email)
        # Pesu_Staff.name=name
        # Pesu_Staff.designation=designation
        # Pesu_Staff.domains=domains
        # Pesu_Staff.education=professor_education
        # Pesu_Staff.experience=professor_experience
        # Pesu_Staff.department=department
        # Pesu_Staff.email=email
        # pesu_staff.campus=campus
        # Pesu_Staff.responsibilities=responsibilities
        return Pesu_Staff


def main():
    StaffPageHandler.get_staff_details()


if __name__ == "__main__":
    main()
