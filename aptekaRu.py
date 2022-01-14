import time
from selenium import webdriver
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.set_capability("general.user.agent",
                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36")

def pars(res):
    url = 'https://apteka.ru/'
    soup = BeautifulSoup(res, 'lxml')
    titles = soup.find_all(class_='catalog-card card-flex')
    mass = []
    for title in titles:
        if title.find('div', class_='card-price__unavailable') != None:
            continue
        try:
            mass.append(str(title.find('em').text) + ' ; ' + str(title.find('span', class_='moneyprice__roubles').text) + 'Р' + ' ; ' + url + str(title.find('a').get('href')))
        except:
            mass.append(str(title.find('a', class_='catalog-card__name emphasis').text) + ' ; ' + str(title.find('span', class_='moneyprice__roubles').text) + 'Р' + ' ; ' + url + str(title.find('a').get('href')))
    return mass

def aptekaRu(msg: str, city: str):
    browser = webdriver.Chrome(
        executable_path=(r"C:\Users\petaa\PycharmProjects\aptekaOPD\chromedriver.exe"),
        options=options
    )
    browser.get('https://apteka.ru/search/?q=' + msg)
    time.sleep(2)
    browser.find_element_by_id("search-city").send_keys(city)
    time.sleep(1)
    browser.find_element_by_class_name('simplebar-content').click()
    time.sleep(1)
    browser.find_element_by_class_name('NotifyCitychange__close').click()
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="app"]/div[5]/div/button').click()
    time.sleep(2)
    browser.find_element_by_class_name("emphasis").click()
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="scrollspy-content"]/div[1]/dl/div[1]/dd/span/a').click()
    time.sleep(2)
    browser.execute_script("window.scrollTo(0, 900)")
    browser.get(str(browser.current_url) + '&sort=byprice')
    time.sleep(2)
    try:
        q = pars(browser.page_source)
        browser.close()
        browser.quit()
    except:
        browser.close()
        browser.quit()
    return q












