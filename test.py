# -*- coding: utf_8 -*-

import os

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from consts import *

fp = webdriver.FirefoxProfile()
fp.accept_untrusted_certs = True
fp.assume_untrusted_cert_issuer = False

# 0:デスクトップ、1:システム規定のフォルファ、2:ユーザ定義フォルダ
fp.set_preference("browser.download.folderList",2)
# 上記で2を選択したのでファイルのダウンロード場所を指定
fp.set_preference("browser.download.dir", os.getcwd())
print(os.getcwd())
fp.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
# ダウンロード完了時にダウンロードマネージャウィンドウを表示するかどうかを示す真偽値。
fp.set_preference("browser.download.manager.showWhenStarting",False)
# mimeタイプを設定
#fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
fp.set_preference("pdfjs.disabled", True)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
driver = webdriver.Firefox(firefox_profile=fp)

#binary = FirefoxBinary()
#driver = webdriver.Firefox(firefox_binary=binary)
driver.get(TARGET_URI)
driver.find_element_by_id('pnEditBox').send_keys('CN103314586')
elements = driver.find_elements_by_class_name('submit')
elements[0].click()
try:
  element = WebDriverWait(driver, 10).until(\
    EC.presence_of_element_located((By.ID, "body"))
  )
finally:
  element = driver.find_element_by_id('publicationId1')
element.click()
driver.implicitly_wait(10)
time.sleep(5)
continue_link = driver.find_element_by_link_text('Global Dossier')
#  element = WebDriverWait(driver, 10).until(\
#    EC.presence_of_element_located(driver.find_element_by_link_text('Global Dossier'))
#  )
continue_link.click()
main_window = driver.current_window_handle
time.sleep(2)
for window in driver.window_handles:
  driver.switch_to.window(window)
  if driver.title == 'European Patent Register':
    break
try:
  element = WebDriverWait(driver, 10).until(\
    EC.presence_of_element_located((By.ID, "row"))
  )
finally:
  elements = driver.find_elements_by_partial_link_text(u"Office Action")
print(len(elements))
#elements[0].click()
sub_window = driver.current_window_handle
i = 0
for element in elements:
  time.sleep(5)
  element.click()
  for window in driver.window_handles:
    driver.switch_to.window(window)
    time.sleep(1)
    if driver.title == 'Register Plus PDF viewer':
      element = WebDriverWait(driver, 60).until(\
        EC.presence_of_element_located((By.ID, "myIframe"))
      )
      iframe = driver.find_element_by_id('myIframe')
      driver.switch_to_frame(iframe)
      element = WebDriverWait(driver, 60).until(\
        EC.presence_of_element_located((By.ID, "toolbarContainer"))
      )
      driver.find_element_by_id('download').click()
      time.sleep(9)
      files0 = filter(os.path.isfile, os.listdir(os.getcwd()))
      files = []
      for f in files0:
        base,ext = os.path.splitext(f)
        if ext == '.pdf':
          files.append(f)
      files = [os.path.join(os.getcwd(), f) for f in files]
      files.sort(key=lambda x: os.path.getmtime(x))
      newest_file = files[-1]
      os.rename(newest_file, os.getcwd()+u"/"+str(i)+u".pdf")
      i += 1
      driver.switch_to.window(window)
      break
  time.sleep(5)
  driver.close()
  driver.switch_to.window(sub_window)
driver.switch_to.window(main_window)

driver.quit()

