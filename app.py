from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import datetime
import time


app = Flask(__name__)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

 
# Chrome 드라이버 생성
browser1 = webdriver.Chrome(options = options)
browser2 = webdriver.Chrome(options = options)


# 요일 List (number got from datetime library)
weekday = { 0: 'Montag', 1: 'Dienstag', 2: 'Mittwoch', 3: 'Donnerstag', 4: 'Freitag' }


# pollen 종류
pollenType = [ 'Ambrosia', 'Ampfer', 'Beifuß', 'Buche', 'Erle', 'Esche', 'Gräser', 'Hasel', 'Pappel', 'Roggen', 'Ulme', 'Wegerich', 'Weide' ]
# pollen 세기
burdenType = { 'noburden': 0, 'weakburden': 1, 'moderateburden': 2, 'strongburden': 3 }
# pollen 종류-세기 딕셔너리 
pollenList = {'Ambrosia': '', 'Ampfer': '', 'Beifuß': '', 'Buche': '', 'Erle': '', 'Esche': '', 'Gräser': '', 'Hasel': '', 'Pappel': '', 'Roggen': '', 'Ulme': '', 'Wegerich': '', 'Weide': ''} 


@app.route('/')
def menu():
  # [ Mensa Today's Menu ]
  # Mensa 페이지 열기
  browser1.get('https://www.studierendenwerk-aachen.de/speiseplaene/academica-w.html')

  today = weekday[datetime.datetime.today().weekday()]

  todayElement = browser1.find_element(By.ID, '{}'.format(today))  # 검색 결과 가져오기
  menus = todayElement.find_elements(By.CLASS_NAME, 'menue-wrapper')

  # todayElement = wait.until(EC.presence_of_element_located((By.ID, '{}'.format(today))))
  # menus = todayElement.find_elements(By.CLASS_NAME, 'menue-wrapper')


  # time.sleep(30)

  # [ Today's Pollen - Aachen ]
  browser2.get('https://www.wetteronline.de/pollenvorhersage?gid=10501&lat=50.783&locationname=Aachen&lon=6.083')
  # time.sleep(20)
  html = browser2.page_source
  soup = BeautifulSoup(html, 'html.parser')
  names = soup.find_all(class_='polle_text')


  for name in names:
    next_sibling = name.find_next_sibling('div') # 'div' 태그를 가진 sibling 찾기
    if next_sibling is not None:
        data_day0 = next_sibling.get('data-day0') # 'data-day0' 속성 값 가져오기
        pollenList[name.text] = burdenType[data_day0]



  return render_template('index.html', menus=menus, pollenList=pollenList)  #검색 결과를 HTML 템플릿에 전달



app.run(debug=True)
