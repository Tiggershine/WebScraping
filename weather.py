from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


app = Flask(__name__)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


# Wetteronline.de - Pollenvorhersage
URL = 'https://www.wetteronline.de/pollenvorhersage?gid=10501&lat=50.783&locationname=Aachen&lon=6.083'
 
# Chrome 드라이버 생성
browser = webdriver.Chrome(options = options)
browser.get(URL)



# pollen 종류
pollenType = [ 'Ambrosia', 'Ampfer', 'Beifuß', 'Buche', 'Erle', 'Esche', 'Gräser', 'Hasel', 'Pappel', 'Roggen', 'Ulme', 'Wegerich', 'Weide' ]
# pollen 세기
burdenType = { 'noburden': 0, 'weakburden': 1, 'moderateburden': 2, 'strongburden': 3 }

# pollen 종류-세기 딕셔너리 
pollenList = {'Ambrosia': '', 'Ampfer': '', 'Beifuß': '', 'Buche': '', 'Erle': '', 'Esche': '', 'Gräser': '', 'Hasel': '', 'Pappel': '', 'Roggen': '', 'Ulme': '', 'Wegerich': '', 'Weide': ''} 


html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
names = soup.find_all(class_='polle_text')


for name in names:
  next_sibling = name.find_next_sibling('div') # 'div' 태그를 가진 sibling 찾기
  if next_sibling is not None:
      data_day0 = next_sibling.get('data-day0') # 'data-day0' 속성 값 가져오기
      pollenList[name.text] = burdenType[data_day0]

print(pollenList)




# get data from wetteronline.de
# pollens = browser.find_element(By.ID, 'bloc_pollen_location')
# names = pollens.find_elements(By.XPATH, '//*[@id="hog_text"]')
# for name in names:
#   print(name.text)

# name = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/div[3]/div[1]/div[2]/div/section[2]/div[3]/div[1]/p')))
# print(name.text + 'str')






# names = pollens.find_elements(By.ID, 'hog_text')
# for name in names:
#   print(name.text)



# for pollen in pollens:
#   name = pollen.find_elements(By.ID, 'hog_text')
#   burden = pollen.find_elements(By.CLASS_NAME, 'noburden').__getattribute__('data-day0')




# for geoName in geoNames:
#   print(geoName)


# for pollen in pollens:
#   pollenType = pollen.find_element(By.CLASS_NAME, 'type').text
#   pollenIntensity = pollen.find_element(By.CLASS_NAME, 'burden').text
#   print("Type: {pollenType} - Intensity: {pollenIntensity}")



