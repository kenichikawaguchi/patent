# -*- coding: utf_8 -*-

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from consts import *

binary = FirefoxBinary()
driver = webdriver.Firefox(firefox_binary=binary)
driver.get(TARGET_URI)

driver.quit()
