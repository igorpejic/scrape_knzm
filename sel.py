from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from bs4 import BeautifulSoup
import time


class ScrapeKonzum:

    def wait_for_element(self, webdriver, path):
        limit = 1800   # waiting limit in seconds
        inc = 0.5   # in seconds; sleep for 500ms
        c = 0
        while (c < limit):
            try:
                print "Waiting... " + str(c)
                webdriver.find_element_by_xpath(path)
                print "Found!"
                return 1
            except Exception:  # the most diabolical python antipattern
                time.sleep(inc)
                c = c + inc
        print "The element hasn't been found."

    def write_to_file(self, file_name, code, profile):
        file_name = file_name + ".txt"
        browser = webdriver.Firefox(profile)
        browser.get('http://online.konzum.hr/#!/categories/{0}/sve-za-dom?show=all&sort_field=name&sort=nameAsc&page=1&per_page=1000000'.format(code))
        self.wait_for_element(browser, "//*[contains(text(), 'Kn/Ko')]")

        soup = BeautifulSoup(browser.page_source)
        browser.close()

        with open(file_name, 'w') as f:
            for item, price, url in zip(soup.select('span[itemprop]'),
                                        soup.select('.price'),
                                        soup.find_all('img')):
                print item.text + " " + price.text + "\n"
                f.write((item.text + " " + price.text +
                         " http://www.online.konzum.hr" + url['src'] +
                         "\n").encode('utf-8'))

    def no_images_download_profile(self):
        """Don't download images"""
        firefox_profile = FirefoxProfile()
        firefox_profile.set_preference('permissions.default.stylesheet', 2)
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference(
            'dom.ipc.plugins.enabled.libflashplayer.so',
            'false'
        )
        return firefox_profile


def main():
    item_codes = {
        "hrana": 60004323,
        "pice": 60005633,
        "sve-za-dom": 60004814,
        "tehnika": 60005133,
        "ljepota-i-njega": 60005472,
        "djecji-svijet": 60005549,
        "igracke": 60005584,
        "knjige": 60005628,
        "vrt-i-kamp": 60005366,
        "tekstil-za-kucanstvo-njega-obuce-carape": 60005273,
        "kucni-ljubimci": 60005258,
        "kiosk": 60005032
    }
    scraper = ScrapeKonzum()
    for key, value in item_codes.items():
        scraper.write_to_file(key, value, scraper.no_images_download_profile())

if __name__ == "__main__":
    main()
