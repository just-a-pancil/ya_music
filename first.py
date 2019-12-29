from selenium.webdriver.chrome import service
import sys
import requests, os, json, time, re, sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from browsermobproxy import Server
from selenium.webdriver.chrome import service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# if len(sys.argv) < 3:
#     print('The syntax should be:')
#     print('%s log pass [n] [s]'%(sys.argv[0]))
#     print('\n\n\tlog - VK login\n\tpass - VK password\n\tn - number of tracks(default 1)\n\ts - number of skips')
#     sys.exit()

link = 'https://music.yandex.ru/home'
track_title = ''
download_flag = 0
# server = Server("/home/duo/Downloads/browsermob-proxy-py/tools/browsermob-proxy-2.1.4/bin/browsermob-proxy")
# server.start()
# proxy = server.create_proxy()
# proxy.new_har()
# Configure the browser proxy in chrome options

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))


driver = webdriver.Chrome(
    "./chromedriver", chrome_options=chrome_options)

driver.get(link)