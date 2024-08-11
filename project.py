from kivy.core.window import Window
Window.clearcolor = (1, 1, 1, 1)
Window.size = (800, 600)
Window.borderless = True
        
from kivy.config import Config
Config.set('graphics', 'width', '800') 
Config.set('graphics', 'height', '600') 

from kivy.uix.image import Image, AsyncImage
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock

import requests
import configparser

count = 0
dish = ""
data = {}
current_recipe = ""
current_image = ""
current_link = ""
current_ingredients = []
recipes = []
images = []
ingredients = []
links = []
to_recipe_screen = False
to_recipe_first_time = True
recipe_count = 0

class MyApp(MDApp):
    def build(self):
        sm = WindowManager()
        sm.add_widget(TitleScreen(name="title"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(RecipeScreen(name="recipe"))
        sm.add_widget(ExitScreen(name="exit"))
        return sm
        
class ImageButton(ButtonBehavior, Image):
    pass

class WindowManager(ScreenManager):
    pass

class TitleScreen(Screen):
    def __init__(self, **kwargs):    
        super(TitleScreen, self).__init__(**kwargs)
        
        layout = FloatLayout()
        
        exit_btn = ImageButton(source="quit.png", size_hint=(None, None), size=(50, 50), pos=(740, 540))
        exit_btn.bind(on_press=self.go_to_exit_screen)
        start_button = ImageButton(source="startbutton.png", size_hint=(None, None), size=(250, 80), pos=(270,30))
        start_button.bind(on_press=self.go_to_main_screen)
        layout.add_widget(exit_btn)
        layout.add_widget(Image(source="foods.png", size_hint=(None, None),size=(400,400), pos=(200, 180)))
        layout.add_widget(Label(text="ReciPY!", color=(0, 0, 0, 1), font_size='45sp', size_hint=(None, None), pos=(350, 110), font_name="oswaldsemibold.ttf"))
        layout.add_widget(start_button)
            
        self.add_widget(layout)
        
    def go_to_exit_screen(self, instance):
        self.manager.current = "exit"
    
    def go_to_main_screen(self, instance):
        self.manager.current = "main"
        
class MainScreen(Screen):
    def __init__(self, **kwargs):    
        super(MainScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        
        title_label = Label(text="ReciPY!", color=(0, 0, 0, 1), font_size='45sp', size_hint=(None, None), pos=(350, 460), font_name="oswaldsemibold.ttf")
        layout.add_widget(title_label)
        
        search_bar = MDTextField(hint_text="Search Recipe", mode="rectangle", line_color_normal=(0,0,0,1), size_hint=(None, None), size=(450,150), pos=(170, 410))
        layout.add_widget(search_bar)
        
        error_label = Label(text="Error! Please input a dish.", color=(0, 0, 0, 1), font_size='25sp', size_hint=(None, None), pos=(350, 230), font_name="oswaldsemibold.ttf")
        layout.add_widget(error_label)
        error_label.opacity = 0
        
        loading_label = Label(text="Fetching Recipes .....", color=(0, 0, 0, 1), font_size='25sp', size_hint=(None, None), pos=(350, 230), font_name="oswaldsemibold.ttf")
        layout.add_widget(loading_label)
        loading_label.opacity = 0
        
        search_button = ImageButton(source="search.png", size_hint=(None, None), size=(100, 100), pos=(350, 320))
        search_button.bind(on_press=lambda *args: self.display_recipe_titles(search_bar.text, dish1_label, dish2_label, dish3_label, dish4_label, dish5_label, error_label, back_button, next_button, search_bar))
        layout.add_widget(search_button)
        
        dish1_label = MDFlatButton(text="", md_bg_color=(0, 0, 0, 0), font_size='22sp', size_hint=(None, None), pos=(280, 290), font_name="oswaldsemibold.ttf")
        dish1_label.bind(on_press=lambda *args: self.go_to_recipe_screen(dish1_label))
        layout.add_widget(dish1_label)
        
        dish2_label = MDFlatButton(text="",  md_bg_color=(0, 0, 0, 0), font_size='22sp', size_hint=(None, None), pos=(280, 240), font_name="oswaldsemibold.ttf")
        dish2_label.bind(on_press=lambda *args: self.go_to_recipe_screen(dish2_label))
        layout.add_widget(dish2_label)
        
        dish3_label = MDFlatButton(text="",  md_bg_color=(0, 0, 0, 0), font_size='22sp', size_hint=(None, None), pos=(280, 190), font_name="oswaldsemibold.ttf")
        dish3_label.bind(on_press=lambda *args: self.go_to_recipe_screen(dish3_label))
        layout.add_widget(dish3_label)
        
        dish4_label = MDFlatButton(text="",  md_bg_color=(0, 0, 0, 0), font_size='22sp', size_hint=(None, None), pos=(280, 140), font_name="oswaldsemibold.ttf")
        dish4_label.bind(on_press=lambda *args: self.go_to_recipe_screen(dish4_label))
        layout.add_widget(dish4_label)
        
        dish5_label = MDFlatButton(text="",  md_bg_color=(0, 0, 0, 0), font_size='22sp', size_hint=(None, None), pos=(280, 90), font_name="oswaldsemibold.ttf")
        dish5_label.bind(on_press=lambda *args: self.go_to_recipe_screen(dish5_label))
        layout.add_widget(dish5_label)
        
        back_button = ImageButton(source="back.png", size_hint=(None, None), size=(40, 40), pos=(350, 40))
        back_button.bind(on_press=lambda *args: self.bck_btn_fnctn(dish1_label, dish2_label, dish3_label, dish4_label, dish5_label, back_button, next_button))
        layout.add_widget(back_button)
        back_button.opacity = 0
        back_button.disabled = True
        
        next_button = ImageButton(source="next.png", size_hint=(None, None), size=(40, 40), pos=(410, 40))
        next_button.bind(on_press=lambda *args: self.nxt_btn_fnctn(dish1_label, dish2_label, dish3_label, dish4_label, dish5_label, back_button, next_button))
        layout.add_widget(next_button)
        next_button.opacity = 0
        next_button.disabled = True
        
        exit_btn = ImageButton(source="exit.png", size_hint=(None, None), size=(30, 30), pos=(20, 540))
        exit_btn.bind(on_press=self.switch_to_title)
        layout.add_widget(exit_btn)
        
        self.add_widget(layout)
        
    def switch_to_title(self, instance):
        self.manager.current = "title"
        
    def store_data(self, dish):
        global data
        global recipes
        global images
        global ingredients
        global links
        
        config = configparser.ConfigParser()
        config.read("config.ini")
        
        access_point = "https://api.edamam.com/api/recipes/v2?type=public"
        app_id= config.get("APPID", "app_id")
        application_keys = config.get("APPKEY", "app_key")
        
        result = requests.get(f"{access_point}&q={dish}&app_id={app_id}&app_key={application_keys}")
        _data = result.json()
        
        data.clear()
        
        data = _data

        recipes.clear()
        images.clear()
        ingredients.clear()
        links.clear()
        
        for i in range(0, len(_data["hits"])):
            recipes.append(_data["hits"][i]["recipe"]["label"])
            images.append(_data["hits"][i]["recipe"]["image"])
            ingredients.append(_data["hits"][i]["recipe"]["ingredientLines"])
            links.append(_data["hits"][i]["recipe"]["url"])
        
        return recipes

    def display_recipe_titles(self, _dish, label1, label2, label3, label4, label5, error_label, back_button, next_button, textfield):
        try:
            global count
            count = 0
            global dish
            dish = _dish
            recipe = self.store_data(dish)
            back_button.opacity = 0
            back_button.disabled = True
            next_button.opacity = 1
            next_button.disabled = False
            error_label.opacity = 0
            textfield.text = "" 
            
            label1.text = recipe[0]
            label2.text = recipe[1]
            label3.text = recipe[2]
            label4.text = recipe[3]
            label5.text = recipe[4]
            
        except IndexError:
            error_label.opacity = 1
            back_button.opacity = 0
            back_button.disabled = True
            next_button.opacity = 0
            next_button.disabled = True
            label1.text = ""
            label2.text = ""
            label3.text = ""
            label4.text = ""
            label5.text = ""
    
    def toggle(self, label1, label2, label3, label4, label5, back_button, next_button):
        global dish
        recipe = self.store_data(dish)
        global count
        
        back_button.opacity = 1
        back_button.disabled = False
        next_button.opacity = 1
        next_button.disabled = False
        
        if count == 0:
            label1.text = recipe[0]
            label2.text = recipe[1]
            label3.text = recipe[2]
            label4.text = recipe[3]
            label5.text = recipe[4]
            back_button.opacity = 0
            back_button.disabled = True
        if count == 1:
            label1.text = recipe[5]
            label2.text = recipe[6]
            label3.text = recipe[7]
            label4.text = recipe[8]
            label5.text = recipe[9]
        elif count == 2:
            label1.text = recipe[10]
            label2.text = recipe[11]
            label3.text = recipe[12]
            label4.text = recipe[13]
            label5.text = recipe[14]
        elif count == 3:
            label1.text = recipe[15]
            label2.text = recipe[16]
            label3.text = recipe[17]
            label4.text = recipe[18]
            label5.text = ""
            next_button.opacity = 0
            next_button.disabled = True
            
    def bck_btn_fnctn(self, label1, label2, label3, label4, label5, back_button, next_button):
        global count
        count -= 1
        self.toggle(label1, label2, label3, label4, label5, back_button, next_button)
        
    def nxt_btn_fnctn(self, label1, label2, label3, label4, label5, back_button, next_button):
        global count
        count += 1
        self.toggle(label1, label2, label3, label4, label5, back_button, next_button)
        
    def go_to_recipe_screen(self, label):
        global current_recipe
        global to_recipe_screen
        current_recipe = label.text
        to_recipe_screen = True
        self.manager.current = "recipe"

class RecipeScreen(Screen):
    def __init__(self, **kwargs):    
        super(RecipeScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()
        Clock.schedule_interval(self.initialize_widgets, 1)
        
    def initialize_widgets(self, instance):
        global current_image
        global current_recipe
        global current_link
        global current_ingredients
        global to_recipe_screen
        global images
        global recipes
        global links
        global ingredients
        global to_recipe_first_time
        
        i = 0
        for recipe in recipes:
            if current_recipe == recipe:
                current_image = images[i]
                current_link = links[i]
                current_ingredients = ingredients[i]
            i += 1
        
        if to_recipe_screen:
            if to_recipe_first_time:
                
                self.recipe_title_lable = Label(text=current_recipe, color=(0, 0, 0, 1), font_size='45sp', size_hint=(None, None), pos=(350, 520), font_name="oswaldsemibold.ttf")
                self.layout.add_widget(self.recipe_title_lable)
                
                self.recipe_image = AsyncImage(source=current_image, size_hint=(None, None), size=(250, 250), pos=(280, 280))
                self.layout.add_widget(self.recipe_image)

                self.link_label = Label(text=f"{current_link}", color=(0, 0, 0, 1), font_size="20sp", size_hint=(None, None), pos=(350, 210), font_name="oswaldsemibold.ttf")
                self.layout.add_widget(self.link_label)
                
                self.ingridients_label = Label(text="ingredients:", color=(0, 0, 0, 1), font_size="19sp", size_hint=(None, None), pos=(350, 180), font_name="oswaldsemibold.ttf")
                self.layout.add_widget(self.ingridients_label)
                
                self.back_to_main_btn = ImageButton(source="exit.png", size_hint=(None, None), size=(30, 30), pos=(20, 540))
                self.back_to_main_btn.bind(on_press=self.bck_2_main_screen)
                self.layout.add_widget(self.back_to_main_btn)
                
                pos_y_1 = 180
            
                self.ingredients_label = []
                
                for i in range(0, 4):
                    self.ingredients_list_label = Label(text="", color=(0, 0, 0, 1), font_size="18sp", size_hint=(None, None), pos=(350, pos_y_1 - 30), font_name="oswaldsemibold.ttf")
                    pos_y_1 -= 30
                    self.ingredients_label.append(self.ingredients_list_label)
                    self.layout.add_widget(self.ingredients_list_label)
                
                for j in range(0, 4):
                    try:
                        self.ingredients_label[j].text = current_ingredients[j]
                    except:
                        continue
                        
                self.back_button = ImageButton(source="back.png", size_hint=(None, None), size=(40, 40), pos=(350, 20))
                self.back_button.bind(on_press=lambda *args: self.bck_fnctn(self.next_button, self.back_button))
                self.layout.add_widget(self.back_button)
                self.back_button.opacity = 0
                self.back_button.disabled = True
            
                self.next_button = ImageButton(source="next.png", size_hint=(None, None), size=(40, 40), pos=(410, 20))
                self.next_button.bind(on_press=lambda *args: self.nxt_fnctn(self.next_button, self.back_button))
                self.layout.add_widget(self.next_button)
                self.next_button.opacity = 0 
                self.next_button.disabled = True
                
                self.add_widget(self.layout)
                to_recipe_screen = False
                to_recipe_first_time = False
            
            else:
                self.recipe_title_lable.text = current_recipe
                self.recipe_image.source = current_image
                self.link_label.text = current_link
                
                print(len(current_ingredients))
                
                if len(current_ingredients) > 4:
                    self.next_button.opacity = 1
                    self.next_button.disabled = False
                    self.back_button.opacity = 0
                    self.back_button.disabled = True
                elif len(current_ingredients) <= 4:
                    self.next_button.opacity = 0
                    self.next_button.disabled = True
                    self.back_button.opacity = 0
                    self.back_button.disabled = True
                    
                
                for i in range(0, 4):
                    try:
                        self.ingredients_label[i].text = ""
                    except IndexError:
                        continue
                
                if len(current_ingredients) <= 4:
                    for i in range(0, len(current_ingredients)):
                        self.ingredients_label[i].text = current_ingredients[i]
                elif len(current_ingredients) > 4:   
                    for i in range(0, 4):
                        self.ingredients_label[i].text = current_ingredients[i]
                
                to_recipe_screen = False
            
    def toggle(self):
        if recipe_count == 0:
            for i in range(0, 4):        
                self.ingredients_label[i].text = current_ingredients[i]
        elif recipe_count == 1:
                for j in range(0, 4):
                    try:
                        self.ingredients_label[j].text = ""
                        self.ingredients_label[j].text = current_ingredients[j + 4]
                    except IndexError:
                        continue
                
    def nxt_fnctn(self, next, back):
        global recipe_count
        recipe_count += 1
        next.opacity = 0
        next.disabled = True
        back.opacity = 1
        back.disabled = False
        self.toggle()
    
    def bck_fnctn(self, next, back):
        global recipe_count
        recipe_count -= 1
        next.opacity = 1
        next.disabled = False
        back.opacity = 0
        back.disabled = True
        self.toggle()
        
    def bck_2_main_screen(self, instance):
        self.manager.current = "main"

class ExitScreen(Screen):
    def __init__(self, **kwargs):    
        super(ExitScreen, self).__init__(**kwargs)
        
        self.layout = FloatLayout()
        
        self.quit_label = Label(text="Do you want to quit?", color=(0, 0, 0, 1), font_size='45sp', size_hint=(None, None), pos=(350, 320), font_name="oswaldsemibold.ttf")
        self.layout.add_widget(self.quit_label)
        
        self.yes_btn = MDFlatButton(text="YES",  md_bg_color=(0, 0, 0, 0), font_size='35sp', size_hint=(None, None), pos=(310, 220), font_name="oswaldsemibold.ttf")
        self.yes_btn.bind(on_press=self.exit_yes)
        self.layout.add_widget(self.yes_btn)

        self.no_btn = MDFlatButton(text="NO", md_bg_color=(0, 0, 0, 0), font_size='35sp', size_hint=(None, None), pos=(410, 220), font_name="oswaldsemibold.ttf")
        self.no_btn.bind(on_press=self.exit_no)
        self.layout.add_widget(self.no_btn)
        
        self.add_widget(self.layout)
            
    def exit_yes(self, instance):
        App.get_running_app().stop()

    def exit_no(self, instance):
        self.manager.current = "title"
        print("Exit")

def main():
    MyApp().run()

if __name__ =="__main__":
    main()