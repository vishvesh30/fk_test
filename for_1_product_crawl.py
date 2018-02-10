import logging
from math import ceil
import json

import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

options = webdriver.FirefoxOptions()
options.set_headless()
# driver1 = webdriver.Firefox()
driver2 = webdriver.Firefox(options=options)

# options = webdriver.ChromeOptions()
# options.binary_location = "C:\\Program Files (x86)\\Opera\\50.0.2762.67\\opera.exe"# path to opera executable
driver3 = webdriver.Firefox(options=options)
final_data = []
# final_data['Product'] = []
product_data = {}
review_title_list = []
review_text_list = []
review_user_list = []
review_date_list = []
review_star_list = []
output_file = open('data.json', 'w', encoding='utf-8')
logging.basicConfig(filename="logs/test.log",format='%(asctime)s %(message)s',filemode='w',level=logging.DEBUG)
logging.info("Program Started")

def product_list():
    url = "https://www.flipkart.com/air-conditioners/pr?sid=j9e,abm,c54&otracker=categorytree"


# driver1.get(url)

# total_string = driver1.find_element_by_xpath('//div[@class="_1JKxvj _31rYcN"]/span/span')
#  page_data = str(total_string.text).split(" ")
#  total_page = int(page_data[3])
#  page_no = 1
#  while page_no <= total_page:
#      print("in while loop product list")
#      temp_url = url + "&page=" + str(page_no) + "&viewType=list"
#      print(temp_url)
#      driver1.get(temp_url)
#      for link_tag in driver1.find_elements_by_class_name("_1UoZlX"):
#          half_link = link_tag.get_attribute("href")
#          product(half_link)
#      print("after for loop")
#      page_no += 1
#  print("exit while loop")


def product(url):
    url = "https://www.flipkart.com/samsung-galaxy-s7-gold-platinum-32-gb/p/itmeuyda4qgqetc6?pid=MOBEGFZPWJHYT7NX&srno=s_1_1&otracker=search&lid=LSTMOBEGFZPWJHYT7NXKNHWSQ&fm=SEARCH&iid=6afd9e5a-2a85-4540-a6c5-3c392fb04712.MOBEGFZPWJHYT7NX.SEARCH&ppt=Search%20Page&ppn=Search%20Page&ssid=n6ypoyuo22c0ugow1518023127500&qH=9d7115b42254d59b"
    driver2.get(url)
    link_tag = driver2.find_element_by_xpath('//div[@class="col _39LH-M"]/a')
    link = str(link_tag.get_attribute("href"))
    total_review_line = link_tag.find_element_by_xpath('//div[@class="swINJg _3nrCtb"]/span')
    count = total_review_line.text.split(" ")
    review_count = int(count[2])
    total_pages = ceil(review_count / 10)
    product_name_tag = driver2.find_element_by_xpath('//h1[@class="_3eAQiD"]')
    product_name = product_name_tag.text
    review(link, total_pages, product_name)


def review(link, total_pages, product_name):
    page = 1
    while page <= total_pages:
        url = link + "&page=" + str(
            page)
        # print(url)
        driver3.get(url)

        for span_more in driver3.find_elements_by_class_name("_1EPkIx"):
            span_more.click()
        for whole_block in driver3.find_elements_by_xpath('//div[@class="col _390CkK"]'):
            uname = whole_block.find_element_by_xpath('div[3] / div[1] / p[1]')
            review_user_list.append(uname.text)
            date = whole_block.find_element_by_xpath('div[3] / div[1] / p[3]')
            formatted_date = datetime.datetime.strptime(date.text, '%d %b, %Y').strftime('%d/%m/%Y')
            review_date_list.append(formatted_date)
            title = whole_block.find_element_by_xpath('div[1] / p')
            review_title_list.append(title.text)
            review_text = whole_block.find_element_by_xpath('div[2] / div / div / div')
            review_text_list.append(review_text.text)
            star_tag = whole_block.find_element_by_xpath('div[1] / div')
            star = star_tag.text.split(" ")
            review_star_list.append(star[0])
        page += 1

    process(product_name)


def process(product_name):
    product_data['review'] = []
    for i in range(len(review_title_list)):
        #     product_data['review'].append({
        #         'Review_title': review_title_list[i],
        #         'Review_text': review_text_list[i]
        #     })
        final_data.append({
            'Name': product_name,
            'Review_title': review_title_list[i],
            'Review_text': review_text_list[i],
            'Review_user': review_user_list[i],
            'Review_date': review_date_list[i],
            'Stars': review_star_list[i]
        })

    review_text_list.clear()
    review_title_list.clear()
    review_user_list.clear()
    review_date_list.clear()
    review_star_list.clear()


def write():
    json.dump(final_data, output_file)
    print(final_data.__len__())


# product_list()
product("hii")
write()
print("exit")
# driver1.close()
driver2.close()
driver3.close()
output_file.close()
logging.info("Program Completed")
