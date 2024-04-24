from bs4 import BeautifulSoup

from pesuacademy.models import SeatingInfo

def get_seating_info_from_page(soup: BeautifulSoup) -> list[SeatingInfo]:
    info_table = soup.find("table", attrs={"id": "seatinginfo"})
    tablebody = info_table.find("tbody")
    tablerows = tablebody.find_all("tr")
    seating_info = []
    for row in tablerows:
        columns = row.find_all("td")
        assn_name = columns[0].text.strip()
        course_code = columns[1].text.strip()
        date = columns[2].text.strip()
        time = columns[3].text.strip()
        terminal = columns[4].text.strip()
        block = columns[5].text.strip()
        seating_info.append(
            SeatingInfo(assn_name, course_code, date, time, terminal, block)
        )
    return seating_info