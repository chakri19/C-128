from bs4 import BeautifulSoup
from flask import request
import time
import csv

start_url = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
browser = request.get(start_url)

time.sleep(10)

brown_dwarf_star_data = []
new_brown_dwarf_star_data = []

header = ["Name", "Distance", "Mass", "Radius"]
brown_dwarf_star_data = []

def scrap():

    for x in range(0,444):
       soup = BeautifulSoup(browser.page_source, "html.parser")
       for ul_tag in soup.find_all("ul", attrs={"class", "exobrown_dwarf_star"}):
           li_tags = ul_tag.find_all("li")
           temp_list = []
           for index, li_tag in enumerate(li_tags):
               if index == 0:
                   temp_list.append(li_tag.find_all("a")[0].contents[0])
               else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
           brown_dwarf_star_data.append(temp_list)
       browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    with open("scraper2.csv", "w") as f:
       csv_writer = csv.writer(f)
       csv_writer.writerow(header)
       csv_writer.writerow(brown_dwarf_star_data)

def scrap_more_data(hyper_link):
    try:
       page = request.get(hyper_link)
       soup = BeautifulSoup(page.content, "html.parser")
       temp_list = []
       for tr_tag in soup.find_all("tr", attrs={"class" : "fact_row"}):
           td_tags = tr_tag.find_all("td")
           for td_tag in td_tags:
               try:
                   temp_list.append(td_tag.find_all("div", attrs={"class" : "value"})[0].contents[0])
               except:
                   temp_list.append("")
       temp_list.append(new_brown_dwarf_star_data)
    
    except:
        time.sleep(1)
        scrap_more_data(hyper_link)

scrap()
for index, data in enumerate(brown_dwarf_star_data):
    scrap_more_data(data[5])
final_data = []
for index, data in enumerate(brown_dwarf_star_data):
    new_brown_dwarf_star_data_element = new_brown_dwarf_star_data[index]
    new_brown_dwarf_star_data_element = [elem.replace("\n", "") for elem in new_brown_dwarf_star_data_element]
    new_brown_dwarf_star_data_element = new_brown_dwarf_star_data_element[:7]
    print(new_brown_dwarf_star_data_element)
    final_data.append(data + new_brown_dwarf_star_data_element)

with open("scrapmoredata.csv", "w") as f:
       csv_writer = csv.writer(f)
       csv_writer.writerow(header)
       csv_writer.writerow(final_data)