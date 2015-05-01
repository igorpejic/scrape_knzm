from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from bs4 import BeautifulSoup
import time
import sys


def WaitForElement(webdriver, path):
    limit = 1800   # waiting limit in seconds
    inc = 0.5   # in seconds; sleep for 500ms
    c = 0
    while (c < limit):
        try:
            print "Waiting... " + str(c)
            yes = webdriver.find_element_by_xpath(path)
            print "Found!"
            return 1
        except:
            time.sleep(inc)
            c = c + inc
    print sys.exc_info()
    print "The element hasn't been found."
    return 0

items = {"kucni-ljubimci": 467}
"""Don't download images"""
firefoxProfile = FirefoxProfile()
firefoxProfile.set_preference('permissions.default.stylesheet', 2)
firefoxProfile.set_preference('permissions.default.image', 2)
firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so',
                              'false')
browser = webdriver.Firefox(firefoxProfile)
i = 1
browser.get('http://online.konzum.hr/#!/categories/60005258/sve-za-dom?show=all&sort_field=name&sort=nameAsc&max_price=300&page={0}&per_page=467'.format(str(i)))
WaitForElement(browser, "//*[contains(text(), 'Kn/Ko')]")

soup = BeautifulSoup(browser.page_source)
browser.close()
f = open('novi-ljubimci.html', 'w')
f.write(browser.page_source.encode('utf-8'))
f.close()

f = open('kucni-ljubimci.txt', 'w')
for item, price, url in zip(soup.select('span[itemprop]'),
                            soup.select('.price'),
                            soup.find_all('img')):
    print item.text + " " + price.text + "\n"
    f.write((item.text + " " + price.text +
             " http://www.online.konzum.hr" + url['src'] + "\n").encode('utf-8'))
f.close()
