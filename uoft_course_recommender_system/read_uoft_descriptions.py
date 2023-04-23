import csv

import requests
from bs4 import BeautifulSoup


def get_data():
    response = requests.get(f"https://engineering.calendar.utoronto.ca/print/view/pdf/search_courses/print_page/debug")
    soup = BeautifulSoup(response.text, 'html.parser')

    file = open("data/uoft_descriptions.csv", 'w+', newline="")
    writer = csv.writer(file)
    names = soup.findAll('div', attrs={"class": "views-row"})
    for name in names:
        split_soup = BeautifulSoup(str(name), 'html.parser')
        course_name = split_soup.findAll('h3')[0].text
        course_desc = split_soup.findAll("p")[0].text

        course_desc = course_desc.replace("\u200b", " ")
        course_name = course_name.replace("\u200b", " ")

        course_desc = course_desc.replace("\u2011", "-")
        course_name = course_name.replace("\u2011", "-")

        course_desc = course_desc.replace("\u03b2", "b")
        course_name = course_name.replace("\u03b2", "b")
        # course_name = course_name.encode("windows-1252").decode("utf-8")
        # course_desc = course_desc.encode("windows-1252").decode("utf-8")
        writer.writerow([course_name, course_desc])


if __name__ == "__main__":
    get_data()
