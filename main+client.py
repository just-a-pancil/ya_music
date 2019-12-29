phone_mode = False
# phone_mode = True

import socket

from kivy.app import App
from kivy.uix.button import Button
from kivy.graphics.vertex_instructions import Triangle
from kivy.config import Config
from kivy.uix.anchorlayout import  AnchorLayout
from kivy.uix.floatlayout import FloatLayout 
from kivy.uix.slider import Slider

# 2340x1080
if not phone_mode:
    Config.set('graphics', "width", 400)
    Config.set('graphics', "height", 866)

class Connection():
    def __init__(self):
        self.HOST = '192.168.0.104'    # The remote host
        self.PORT = 59090              # The same port as used by the server
        self.sock = None
        #     sock.connect((HOST, PORT))
        #     mes = input('Type smth: ')
        #     mes = mes.encode('utf-8')
        #     sock.sendall(mes)
    def connect(self):
        try:
            self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.HOST, self.PORT))
            return True
        except:
            return None

    def send_mes(self, command='plause'):
        mes = str(command).encode('utf-8')
        # while True:
        self.sock.send(mes)        
        #     self.data = self.sock.recv(1024)
        #     if self.data == mes:
        #         break

class MyButton(Button):
    def __init__(self, layout=None, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.layout = layout

    def remove_myself(self):
        self.layout.remove_widget(self)
        

class myApp(App):


    def __init__(self):
        super(myApp, self).__init__()
        self.conn = Connection()
        self.connected = False

    def start_btn_press(self, instance):
        print('strart_pressed')
        while True:
            if self.conn.connect():
                self.connected = True
                break
        if phone_mode:
            instance.remove_myself()

    def left_btn_press(self, instance):
        print('left_pressed')
        if self.connected:
            self.conn.send_mes('previous')
        else: pass

    def right_btn_press(self, instance):
        print('right_pressed')
        if self.connected:
            self.conn.send_mes('nxt')
        else: pass

    def pause_btn_press(self, instance):
        print('pause_pressed')
        if self.connected:
            self.conn.send_mes()
        else: pass

    def shffle_btn_press(self, instance):
        print('shffle_press')
        if self.connected:
            self.conn.send_mes('shffle')
        else: pass

    def slider_move(self, instance, value):
        self.loudness_value = round(value,2)
        print(self.loudness_value)
        
        

    def loud_btn_press(self, instance):
        print('loud_press')
        mes = str(round(self.loudness_value,2))
        mes = 'loudness ' + mes
        if self.connected:
            self.conn.send_mes(mes)
        else: pass


        
    def build(self):
        global_layout = FloatLayout()
        layout_start =  AnchorLayout(size=(300, 300))
        layout_start.add_widget(MyButton(
            layout=layout_start,
            text='start!', 
            background_color=[0,0,0.5,0.9], 
            background_normal='',
            size_hint=(.3,.1),
            on_press=self.start_btn_press))



        layout_left =  AnchorLayout(size=(300, 300),
            padding=[15,0,0,15],
            anchor_y='bottom', 
            anchor_x='left')
        layout_left.add_widget(MyButton(
            # pos=(100, 100),
            text='previous', 
            background_color=[0,0,0.5,0.9], 
            background_normal='',
            size_hint=(.2,.1),
            on_press=self.left_btn_press))

        layout_right =  AnchorLayout(size=(300, 300),
            padding=[0,0,15,15],
            anchor_y='bottom', 
            anchor_x='right')
        layout_right.add_widget(Button(text='next', 
            background_color=[0,0,0.5,0.9], 
            background_normal='',
            # background_disabled_normal='',
            size_hint=(.2,.1),
            on_press=self.right_btn_press))

        layout_pause = AnchorLayout(
            size=(300, 300),
            padding=[0,0,0,15],
            anchor_y='bottom', 
            anchor_x='center')
        layout_pause.add_widget(Button(text='play/pause', 
            background_color=[0,0,0.5,0.9], 
            background_normal='',
            # background_disabled_normal='',
            size_hint=(.2,.1),
            on_press=self.pause_btn_press))

        layout_shffle = FloatLayout(size=(300, 300))
        layout_shffle.add_widget(Button(
            text='shuffle', 
            background_color=[0,0,0.5,0.9], 
            background_normal='',
            size_hint=(.2,.1),
            on_press=self.shffle_btn_press,
            pos_hint={'x':.40, 'y':.2}
            # pos=(400*.5-400*.5*.5,866/3)
            ))
        layout_slider = AnchorLayout(
            size=(20,20),
            anchor_y='center', 
            anchor_x='right',
            padding=[330    ,100,0,100])
        slider = Slider(
            value_track=True,
            orientation='vertical',
            # sensitivity='handle',
            # border_vertical=[1,1,1,1],
            step=.1,
            # pos_hint={'x':.5, 'y':.005},
            pos=(150,100),
            # padding=1,
            min=0,
            max=100,
            value=25,
            )

        slider.bind(value=self.slider_move)
        layout_slider.add_widget(slider)


        layout_loud = AnchorLayout(
            size=(300, 300),
            anchor_y='center', 
            anchor_x='left',
            padding=[15,0,0,0]
            )
        layout_loud.add_widget(MyButton(
            # pos=(100, 100),
            text='send', 
            background_color=[0,0,0.5,0.9], 
            background_normal='',
            size_hint=(.2,.1),
            on_press=self.loud_btn_press))

        global_layout.add_widget(layout_start)
        global_layout.add_widget(layout_left)
        global_layout.add_widget(layout_right)
        global_layout.add_widget(layout_pause)
        global_layout.add_widget(layout_shffle)
        global_layout.add_widget(layout_slider)
        global_layout.add_widget(layout_loud)


        return global_layout




if __name__ == '__main__':
    myApp().run()