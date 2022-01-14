from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import select
from selenium.webdriver.support.select import Select
import time

options = webdriver.ChromeOptions()
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.set_capability("general.user.agent",
                       "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Mobile Safari/537.36")

def pars(res):
    soup = BeautifulSoup(res, 'lxml')
    cards = soup.find_all(class_='cc-item')
    mass = []
    for card in cards:
        mass.append(str(card.find('a',class_='cc-item--title').text).strip()+' ; '+str(card.find('span',class_='price--num').text).strip() + 'Р' + ' ; ' + str(card.find('meta',itemprop='url').get('content')))
    return mass

def SberEapteka(text: str, city: str):
    browser = webdriver.Chrome(
        executable_path=(r"C:\Users\petaa\PycharmProjects\aptekaOPD\chromedriver.exe"),
        options=options
    )
    browser.maximize_window()
    browser.get('https://www.eapteka.ru/search/?q=' + text)
    time.sleep(2)
    try:
        browser.find_element_by_xpath('//*[@id="headerCity-root-bubble"]/div/div/div/button').click()
        time.sleep(2)
        browser.find_element_by_class_name('header__tower-input').send_keys(city)
        time.sleep(2)
        browser.find_element_by_class_name('header__tower-link').click()
        time.sleep(4)
        browser.find_element_by_xpath('//*[@id="headerCity-root-bubble"]/div/div/a').click()
        time.sleep(4)
    except:
        browser.find_element_by_xpath('//*[@id="headerCity-root-bubble"]/div/button').click()
        time.sleep(4)
    ok = browser.find_element_by_xpath('//*[@id="notifications-root"]/ul/li[1]/div/div/div/div/div/div/a').click()
    time.sleep(4)
    #close = browser.find_element_by_class_name('notification__close').click()
    time.sleep(4)
    try:
        ags = browser.find_element_by_xpath(
            '/html/body/section/div/div[1]/div[3]/div/div[4]/section[1]/div[2]/div[1]/p[4]/a').click()
    except:
        time.sleep(4)
        try:
            ags = browser.find_element_by_xpath('/html/body/section/div/div[1]/div[3]/div/div[2]/section[1]/div[2]/div[1]/p[4]/a').click()
            time.sleep(2)
        except:
            ags = browser.find_element_by_xpath(
                '/html/body/section/div/div[1]/div[3]/div/div[2]/section[1]/div[2]/div[1]/p[3]/a').click()
    time.sleep(2)
    lc = browser.current_url
    browser.get(str(lc) + '/?sort=price&order=asc')
    time.sleep(2)
    try:
        items = pars(browser.page_source)
        browser.close()
        browser.quit()
    except:
        browser.close()
        browser.quit()
    return items

