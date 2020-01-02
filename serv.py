# Echo server program
from selenium.webdriver.chrome import service
from subprocess import call
import time
# import requests, os, json, time, re, sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.chrome import service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import socket


class Server:
    def __init__(self, PORT=59090):
        self.HOST = '192.168.0.104'
        self.PORT = PORT
    def init(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.bind((self.HOST, self.PORT))
        except:
            self.sock.close()
            return None
        return True
    def listen(self):
        self.sock.listen(1)
        self.conn, self.addr = self.sock.accept()
        print('Connected by', self.addr)
        return True
    def recieving(self):
        while True:
            data = self.conn.recv(1024)
            if not data: break
            # self.sock.send(data)
            return data
            # print(data.decode())
        self.conn.close()
        return False


class Browser():
    def __init__(self,
        link='https://music.yandex.ru/users/mrazvozov2015'):
        self.funcs = {}
        self.link = link
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option('w3c', False)
        self.driver = webdriver.Chrome(
            "/home/duo/ya_music/chromedriver",
            options=self.chrome_options)
        self.funcs['previous'] = self.previous
        self.funcs['plause'] = self.plause
        self.funcs['nxt'] = self.nxt
        self.funcs['shffle'] = self.shffle
        self.funcs['loudness'] = self.loudness
        self.funcs['mute'] = self.mute
        self.muted = False
        self.loudness_val = 20

    def run(self, data):
        if data.find(b" ") == -1:
            self.funcs[data.decode()]()
        else:
            splitted_data = data.split()
            self.funcs[splitted_data[0].decode()](
                splitted_data[1].decode(),
                # splitted_data[2].decode()
                )


    def previous(self):
        # prev = self.driver.find_element(
        #         By.XPATH, '//*[@class="d-icon d-icon_track-prev"]')
        # prev.click()
        ActionChains(self.driver).key_up("K").perform()

    def nxt(self):
        # n = self.driver.find_element(
        #         By.XPATH, '//*[@class="d-icon d-icon_track-next"]')
        # n.click()
        ActionChains(self.driver).key_up("L").perform()

    def plause(self):
        # play = self.driver.find_element(
        #         By.XPATH, '//*[@class="d-icon d-icon_play"]')
        # play.click()
        ActionChains(self.driver).key_up("P").perform()

    def login(self, log='mrazvozov2015@yandex.ru',
        pas='qwertyuiop[]asdfghjkl;'):
        self.usr = log[:log.find('@')]
        # login_button = self.driver.find_element_by_name("Войти")
        # login_button.click()
        self.driver.get(r'''https://passport.yandex.ru/auth?
origin=music_button-header&retpath=https%3A%2F%
2Fmusic.yandex.ru%2Fsettings%3Ffrom-passport''')
        login = self.driver.find_element_by_name("login")
        login.send_keys(log+u'\ue007')
        self.driver.implicitly_wait(2)
        pasw =   self.driver.find_element_by_name("passwd")
        pasw.send_keys(pas+u'\ue007')
        return WebDriverWait(self.driver, 10).until(EC.url_matches('/account'))
            
        
    def play_fav(self):
        self.driver.get('https://music.yandex.ru/users/%s/playlists/3'
            %(self.usr))
        butt = self.driver.find_element(By.XPATH, '//*[@class="d-track__start-column"]')
        a = ActionChains(self.driver)
        a.move_to_element(butt)
        a.move_by_offset(0,1)
        a.pause(0.5)
        a.double_click()
        a.perform()

    def shffle(self):
        try:
            butt = self.driver.find_element(
            By.XPATH, '//*[@class="d-icon d-icon_shuffle"]')
        except:
            butt = self.driver.find_element(
            By.XPATH, '//*[@class="d-icon d-icon_shuffle-gold"]')
        finally:
            pass
        butt.click()

    def mute(self):
        # play = self.driver.find_element(
        #         By.XPATH, '//*[@class="volume__btn"]')
        # play.click()
        self.loudness(0)

    def loudness(self, value=None, check_val=None):
        # call((["amixer", "sset", "Master", "1%+"]))
        if type(value) == str:
            if value == '+':
                ActionChains(self.driver).key_up("+").perform()
            elif value == '-':
                ActionChains(self.driver).key_up("-").perform()
        elif type(value) == int:
            ActionChains(self.driver).key_up("0").perform()
            for i in range(round(value/10)):
                ActionChains(self.driver).key_up("+").perform()
                ActionChains(self.driver).pause(.05).perform()
        print('loudness ' + str(value))

    def test(self):
        pass

serv = Server()
while True:
    if serv.init(): break

if serv.listen():
    browser = Browser()
    browser.login(log='iwannabeyourgirlfriend@yandex.ru',
        pas='PASSPORT_1WanNaBUrGf_YANDEX')
    browser.play_fav()
    # browser.plause()
    browser.loudness(20)


while True:
    data = serv.recieving()
    if not data: break
    print(data.decode())
    browser.run(data)

# browser.driver.quit()