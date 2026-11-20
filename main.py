from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Color,Ellipse,Rectangle,RoundedRectangle,Line
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
import os
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
import random
from kivy.graphics.texture import Texture
import sqlite3
from kivy.utils import platform
#================================
if platform=='android':
    pass
else:
    Window.size=(480,800)
#================================
# Database class
class Musicdatabase:
    def __init__(self):
        self.conn=sqlite3.connect('my_ringtones.db')
        self.cursor=self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ringtones (id INTEGER PRIMARY KEY AUTOINCREMENT, song_name TEXT, file_path TEXT)''')
        self.conn.commit()
    def add_song(self,name,path):
        self.cursor.execute('INSERT INTO ringtones (song_name,file_path) VALUES (?,?)',(name,path))
        self.conn.commit()
    def get_all_songs(self):
        self.cursor.execute('SELECT song_name,file_path FROM ringtones')
        return self.cursor.fetchall()
db=Musicdatabase()
#================================
# Kivy RGBA format colors
gradient_pairs = [
    # (Dark Base, Neon Highlight)
    ((0.1, 0.1, 0.3, 1), (0.2, 0.8, 0.9, 1)), # 1. Deep Blue -> Cyan
    ((0.2, 0.0, 0.3, 1), (0.9, 0.2, 0.5, 1)), # 2. Dark Purple -> Neon Pink
    ((0.3, 0.0, 0.1, 1), (0.9, 0.4, 0.2, 1)), # 3. Maroon -> Glowing Orange
    ((0.0, 0.2, 0.2, 1), (0.3, 0.9, 0.5, 1)), # 4. Deep Teal -> Lime Green
    ((0.1, 0.1, 0.1, 1), (0.8, 0.8, 0.8, 1)), # 5. Charcoal -> Silver/White
    ((0.2, 0.1, 0.0, 1), (0.9, 0.8, 0.2, 1)), # 6. Deep Brown -> Shiny Gold
    ((0.1, 0.2, 0.4, 1), (0.5, 0.5, 1.0, 1)), # 7. Navy -> Soft Violet
    ((0.3, 0.1, 0.3, 1), (1.0, 0.4, 0.7, 1)), # 8. Dark Magenta -> Coral Pink
    ((0.0, 0.1, 0.3, 1), (0.4, 0.9, 0.8, 1)), # 9. Ocean Dark -> Mint Green
    ((0.2, 0.0, 0.0, 1), (0.9, 0.2, 0.2, 1)),  # 10. Blood Red -> Hot Red
    ((0.1, 0.1, 0.4, 1), (0.9, 0.5, 0.4, 1)), # 11. Dark Indigo -> Peach/Pink (Sunset)
    ((0.1, 0.0, 0.2, 1), (0.2, 0.9, 0.4, 1)), # 12. Deep Purple -> Neon Green (Cyberpunk)
    ((0.0, 0.1, 0.2, 1), (0.1, 0.8, 0.8, 1)), # 13. Midnight Blue -> Aqua (Ocean)
    ((0.2, 0.0, 0.1, 1), (0.8, 0.2, 0.8, 1)), # 14. Blackberry -> Bright Magenta
    ((0.3, 0.0, 0.0, 1), (0.9, 0.7, 0.1, 1)), # 15. Deep Ruby -> Warm Yellow (Golden)
    ((0.1, 0.1, 0.1, 1), (0.6, 1.0, 0.2, 1)), # 16. Dark Grey -> Acid Green (Toxic)
    ((0.15, 0.05, 0.2, 1), (0.7, 0.5, 1.0, 1)), # 17. Dark Violet -> Lavender (Amethyst)
    ((0.05, 0.05, 0.05, 1), (0.8, 0.1, 0.2, 1)), # 18. Pitch Black -> Crimson (Blood Moon)
    ((0.0, 0.2, 0.1, 1), (0.4, 0.9, 0.6, 1)),  # 19. Dark Emerald -> Glowing Mint
    ((0.05, 0.1, 0.3, 1), (1.0, 0.1, 0.6, 1)) # 20. Navy -> Hot Pink (Cosmic)
]
#================================
# Making gradient
class gradient(Button):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.background_normal=""
        self.background_color=(0,0,0,0)
        pair=random.choice(gradient_pairs)
        c2=pair[0]
        c1=pair[1]
        self.tex=Texture.create(size=(1,2),colorfmt='rgba')
        self.tex.min_filter='linear'
        self.tex.mag_filter='linear'
        p1=[int(v*255)for v in c1]
        p2=[int(v*255)for v in c2]
        buf=p1+p2
        self.tex.blit_buffer(bytes(buf), colorfmt='rgba',bufferfmt='ubyte')
        with self.canvas.before:
            Color(c1[0],c1[1],c1[2],0.3)
            self.glow=RoundedRectangle(size=self.size,pos=self.pos,radius=[12])
            Color(1,1,1,1)
            self.rect=RoundedRectangle(size=self.size,pos=self.pos,radius=[10],texture=self.tex)
            Color(1,1,1,0.15)
            self.highlight2=RoundedRectangle(size=(self.width,self.height*0.1),pos=(self.x,self.y+self.height*0.9),radius=[10,10,0,0])
            Color(1,1,1,0.3)
            self.highlight=Line(rounded_rectangle=(self.pos[0],self.pos[1],self.width,self.height,10),width=1.2)
        self.bind(pos=self.update_graphics,size=self.update_graphics)
    def update_graphics(self,*args):
        self.glow.pos=(self.pos[0]-2,self.pos[1]-2)
        self.glow.size=(self.size[0]+4,self.size[1]+4)
        self.rect.pos=self.pos
        self.rect.size=self.size
        self.highlight2.size=(self.size[0],self.size[1]*0.1)
        self.highlight2.pos=(self.pos[0],self.pos[1]+self.size[1]*0.9)
        self.highlight.rounded_rectangle=(self.pos[0],self.pos[1],self.size[0],self.size[1],10)
    def change_color(self):
        pair=random.choice(gradient_pairs)
        c2=pair[0]
        c1=pair[1]
        buf=[int(v*255)for v in c1]+[int(v*255)for v in c2]
        self.tex.blit_buffer(bytes(buf),colorfmt='rgba',bufferfmt='ubyte')
        self.canvas.ask_update()
#================================
# Starter
class Ringtoneapp(App):
    def build(self):
        self.layout=FloatLayout()
        w,h=Window.size
        self.song_file=[]
        Clock.schedule_once(self.ask_name,1)
        self.current_sound=None
#================================
# App name and his background
        with self.layout.canvas:
            Color(1,0,0,1)
            self.header_rect=Rectangle(pos=(0,h*0.94),size=(w,h*0.1))
        def update_rectangle(instance,value):
            self.header_rect.pos=(0,instance.height*0.94)
            self.header_rect.size=(instance.width,instance.height*0.1)
        self.layout.bind(pos=update_rectangle,size=update_rectangle)
#_________________________________________
        text=Label(text="My Ringtones", font_size=50,pos_hint={'center_x':0.36, 'center_y':0.97})
        info_text=Label(text="*Phone ringtone max limit is 30-40 sec",font_size=20,color=(0.7,0.7,0.7,1),pos_hint={'center_x':0.5,'center_y':0.93},size_hint_x=1,text_size=(w,None),halign='center')# Ringtone limit info
#_________________________________________
        self.layout.add_widget(text)
        self.layout.add_widget(info_text)
#================================
# Hamburger menu button
        button_1=Button(text="=", font_size=50,size_hint=(0.14,0.06), pos_hint={'center_x':0.06,'center_y':0.97},background_color=(0,1,0,1))
#_________________________________________
        self.layout.add_widget(button_1)
#================================
# Scroll logic and his box logic
        self.scroll=ScrollView(size_hint=(1,0.9),pos_hint={'x':0,'y':0})
        self.song_list=BoxLayout(orientation='vertical',size_hint_y=None,padding=20,spacing=20)
        self.song_list.bind(minimum_height=self.song_list.setter('height'))
#_________________________________________
        self.scroll.add_widget(self.song_list)
        self.layout.add_widget(self.scroll)
#================================
# Import button and his background
        button_2=Button(text="+", font_size=50,size_hint=(None,None),size=(100,100),pos_hint={'center_x':0.85,'center_y':0.12},background_color=(0,0,0,0))
#_________________________________________
        with button_2.canvas.before:
            Color(0,0.8,0,1)
            self.circle=Ellipse(pos=button_2.pos,size=button_2.size)
        def update_circle(instance,value):
            self.circle.pos=instance.pos
            self.circle.size=instance.size
        button_2.bind(pos=update_circle,size=update_circle)
        button_2.bind(on_release=self.open_filemanager)
        self.layout.add_widget(button_2)
#================================
# Blocker
        self.blocker=Button(size_hint=(1,1),background_color=(0,0,0,0.5),opacity=0,pos_hint={'x':2,'y':0})
#_________________________________________
        self.blocker.bind(on_release=self.toggle_menu)
        self.layout.add_widget(self.blocker)
#================================
# Slide panel and name show logic
        self.slide_panel=BoxLayout(orientation='vertical',size_hint=(0.6,1),pos_hint={'x':-1,'y':0},padding=[20,50,20,20])
        with self.slide_panel.canvas.before:
            Color(0.1,0.1,0.1,1)
            self.slide_rect=Rectangle(pos=self.slide_panel.pos,size=self.slide_panel.size)
        def update_slide_rect(instance,value):
            self.slide_rect.pos=instance.pos
            self.slide_rect.size=instance.size
#_________________________________________
        self.slide_panel.bind(pos=update_slide_rect,size=update_slide_rect)
#================================
        self.profile_name=Label(text="Guest",font_size=40,size_hint_y=None,height=100,color=(1,0,0,1)) # user name color
#================================
# Version label
        self.show_version=Label(text="V 1.0",font_size=40,size_hint_y=0.1,size_hint_x=1.6,height=0,color=(0,1,0,1))
#================================
# Profile circle
        user_profile=Button(size_hint=(None,None),size=(200,200),pos_hint={'center_x':0.5,'y':0},background_color=(0,0,0,0))
#_________________________________________
        with user_profile.canvas.before:
            Color(1,0,0,1)
            self.profile_circle=Ellipse(pos=user_profile.pos,size=user_profile.size)
        def update_user_profile(instance,value):
            self.profile_circle.pos=instance.pos
            self.profile_circle.size=instance.size
        user_profile.bind(pos=update_user_profile,size=update_user_profile)
        #user_profile.bind(on_release=self.EDIT_PROFILE) ''' For version 2.0 '''
#_________________________________________
        self.slide_panel.add_widget(user_profile)
        self.slide_panel.add_widget(self.profile_name)
        self.slide_panel.add_widget(Label())
        self.slide_panel.add_widget(self.show_version)
        self.layout.add_widget(self.slide_panel)
        self.menu_open=False
        button_1.bind(on_release=self.toggle_menu)
#================================
# Mini player
        self.mini_player=BoxLayout(orientation='horizontal',size_hint=(1,None),height=120,padding=15,spacing=15,pos_hint={'x':0,'y': 1})
        # mini player color logic
        with self.mini_player.canvas.before:
            Color(0.2,0.2,0.2,1)
            self.mini_rect=Rectangle(pos=self.mini_player.pos,size=self.mini_player.size)
        def update_mini_rect(instance,value):
            self.mini_rect.pos=instance.pos
            self.mini_rect.size=instance.size
        self.mini_player.bind(pos=update_mini_rect, size=update_mini_rect)
# Dummy profile
        self.dummy_profile=gradient(size_hint=(None,None),size=(90,90))
# Song name
        self.playing_song_name=Label(text="Playing song"*3,bold=True,font_size=35,color=(1,1,1,1),text_size=(None,None),size=(500,40))
        anim=Animation(x=-200,duration=4)
        anim+=Animation(x=w,duration=0)
        anim.repeat=True
        anim.start(self.playing_song_name)
# Controls layout
        controls_layout=BoxLayout(orientation='horizontal',size_hint=(None,1),width=250,spacing=10)
        # Button
        self.prev_btn=Button(text="|<",background_color=(0.2,0.5,0.8,1))
        self.stop_btn=Button(text="||",background_color=(0.8,0.1,0.1,1))
        self.stop_btn.bind(on_release=self.stop_audio)
        self.next_btn=Button(text=">|",background_color=(0.2,0.5,0.8,1))
        # Buttons add in controls layout
        controls_layout.add_widget(self.prev_btn)
        controls_layout.add_widget(self.stop_btn)
        controls_layout.add_widget(self.next_btn)
# Packing all thinks in box
        self.mini_player.add_widget(self.dummy_profile)
        self.mini_player.add_widget(self.playing_song_name)
        self.mini_player.add_widget(controls_layout)
# Ringtone set button
        self.set_ring_btn=Button(text="+",bold=True,background_color=(0,0.7,0.2,1),size_hint_x=0.25,size_hint_y=0.08,pos_hint={'center_x':0.18,'center_y':-0.2})
        self.set_ring_btn.bind(on_release=self.set_as_ringtone)
        self.layout.add_widget(self.set_ring_btn)
#_________________________________________
        self.layout.add_widget(self.mini_player)
#================================
# Old song finder
        for name,path in db.get_all_songs():
            self.song_file.append(name)
            self.create_song_button(name,path)
#================================
        return self.layout # builed yaha katam
#================================
# Ask name popup
    def ask_name(self,dt):
        box=BoxLayout(orientation='vertical',padding=20,spacing=20)
        self.name_input=TextInput(hint_text="Enter your name",font_size=40,size_hint_y=None,height=100)
        save_button=Button(text="Save",font_size=30,size_hint_y=None,height=100,background_color=(0,0,1,1))
        box.add_widget(self.name_input)
        box.add_widget(save_button)
#_________________________________________
        self.name_popup=Popup(title="Welcome",content=box,size_hint=(0.8,0.4),auto_dismiss=False)
        save_button.bind(on_release=self.save_name)
        self.name_popup.open()
# what if user what do 
    def save_name(self,instance):
        self.user_name=self.name_input.text
        if self.user_name.strip()=="":
            self.user_name="Master"
        self.profile_name.text=f"Hello,\n{self.user_name}"
        self.name_popup.dismiss()
        print(f"User name is {self.user_name}")
#================================
# Permissions logic
    def on_start(self):
        try:
            if platform == 'android':
                from android.permissions import request_permissions, Permission
                request_permissions([Permission.READ_EXTERNAL_STORAGE,Permission.WRITE_EXTERNAL_STORAGE])
        except Exception as e:
            print("Permission error ignore kiya:", e)
#================================
# Slide blocker animation
    def toggle_menu(self,instance):
        if not self.menu_open:
            anim=Animation(pos_hint={'x':0},duration=0.3)
            anim.start(self.slide_panel)
            self.blocker.pos_hint={'x':0,'y':0}
            self.blocker.opacity=1
            self.menu_open=True
        else:
            anim=Animation(pos_hint={'x':-1},duration=0.3)
            anim.start(self.slide_panel)
            self.blocker.pos_hint={'x':2,'y':0}
            self.blocker.opacity=0
            self.menu_open=False
#================================
# Filemanager opener and file chooser
    def open_filemanager(self,instance):
        self.file_chooser=FileChooserListView(filters=['*.mp3','*.wav','*.ogg'],path='/storage/emulated/0/Download')
        self.file_chooser.bind(selection=self.select_file)
        self.popup=Popup(title="File Manager",content=self.file_chooser, size_hint=(0.9,0.9))
        self.popup.open()
    def select_file(self,filechooser, selection):
        if not selection:
            return
        file_path=selection[0]
        file_name=os.path.basename(file_path)
        if file_name in self.song_file:
            self.show_toast("This file already exists!")
            Clock.schedule_once(lambda dt: setattr(filechooser,'selection',[]),0.1)
            Clock.schedule_once(lambda dt: self.popup.dismiss(),0.1)
            return
        self.song_file.append(file_name)
        db.add_song(file_name, file_path)
        self.show_toast("Saved")
        self.create_song_button(file_name,file_path)
        Clock.schedule_once(lambda dt: self.popup.dismiss(),0.1)
        Clock.schedule_once(lambda dt: setattr(filechooser,'selection',[]),0.1)
#================================
# Song label button
    def create_song_button(self,name, path):
        song_btn=Button(text=name,font_size=40,color=(1,1,1,1),size_hint_y=None,height=80,background_color=(0,0,0,0))
        song_btn.song_path=path
        song_btn.bind(on_release=self.play_sound)
        self.song_list.add_widget(song_btn)
#================================
# Song play and lift logic and stop button
    def play_sound(self,instance):
        if self.current_sound:
            self.current_sound.stop()
            self.reset_button()
        self.dummy_profile.change_color()
        self.current_sound=SoundLoader.load(instance.song_path)
        if self.current_sound:
            self.current_sound.play()
            self.mini_player.pos_hint={'x':0,'y':0}
            self.mini_player.opacity=1
            self.playing_song_name.text=instance.text
            print(f"play:{instance.text}")
            anim_pop=Animation(font_size=55,background_color=(0.2,0.8,0.2,0.4),color=(0,1,0,1),duration=0.2)
#_________________________________________
            anim_pop.start(instance)
            anim_btn_up=Animation(pos_hint={'center':0.18,'center_y':0.22},duration=0.2)
            anim_btn_up.start(self.set_ring_btn)
            self.active_btn=instance
            self.current_sound.bind(on_stop=self.reset_button)
#_________________________________________
    def reset_button(self,*args):
        if hasattr(self,'active_btn')and self.active_btn:
             anim_reset=Animation(font_size=40,background_color=(0,0,0,0),color=(1,1,1,1),duration=0.2)
             anim_reset.start(self.active_btn)
             anim_btn_down=Animation(pos_hint={'center_x':0.18,'center_y':-0.2},duration=0.2)
             anim_btn_down.start(self.set_ring_btn)
             self.active_btn=None
             self.mini_player.pos_hint={'x':0,'y':0}
             self.mini_player.opacity=0
#================================
# Stop logic
    def stop_audio(self,*args):
        if hasattr(self,'current_sound')and self.current_sound:
            self.current_sound.stop()
            self.reset_button()
            print("are print kar hi kyu h")            
#================================
# Toast
    def show_toast(self,message):
        toast=Button(text=message,size_hint=(None,None),size=(400,80),pos_hint={'center_x':0.5,'y':0.1},background_color=(0.2,0.2,0.2,1),disabled=True,background_disabled_normal='',color=(1,1,1,1))
#_________________________________________
        self.layout.add_widget(toast)
        anim=Animation(opacity=1,duration=2)+Animation(opacity=0,duration=2)
        anim.bind(on_complete=lambda*x:self.layout.remove_widget(toast))
        anim.start(toast)
#================================
    def set_as_ringtone(self,*args):
        if not hasattr(self,'active_btn')or not self.active_btn:
            return
        song_path=self.active_btn.song_path
        if platform=='android':
            try:
                from jnius import autoclass
                RingtoneManager=autoclass('android.media.RingtoneManager')
                File=autoclass('java.io.File')
                Uri=autoclass('android.net.Uri')
                PythonActivity=autoclass('org.kivy.android.PythonActivity')
                ringtone_file=File(song_path)
                uri=Uri.parse("file://"+ringtone_file.getAbsolutePath())
                RingtoneManager.setActualDefaultRingtoneUri(PythonActivity.mActivity.getApplicationContext(),RingtoneManager.TYPE_RINGTONE,uri)
                self.show_toast("Ringtone is set")
                print("Android par ringtone set done!")
            except Exception as e:
                error_str = str(e)
                if "SecurityException" in error_str or "settings" in error_str.lower() or "permission" in error_str.lower():
                    from jnius import autoclass
                    Settings = autoclass('android.provider.Settings')
                    Intent = autoclass('android.content.Intent')
                    Uri = autoclass('android.net.Uri')
                    PythonActivity = autoclass('org.kivy.android.PythonActivity')
                    activity = PythonActivity.mActivity
                    intent = Intent(Settings.ACTION_MANAGE_WRITE_SETTINGS)
                    intent.setData(Uri.parse("package:" + activity.getPackageName()))
                    activity.startActivity(intent)
                    self.show_toast("Permission On karein aur wapas button dabayein!")
                else:
                    self.show_toast(error_str)
                    print("Error:", e)
        else:
            self.show_toast("PC Test: Ringtone Set!")
            print(f"PC Test: File '{song_path}' phone mein lag jayegi.")
#================================
# Abhi bhi nhi samaj aya ki ye kya h
if __name__=="__main__":
    Ringtoneapp().run()
#================================