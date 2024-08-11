import unittest
from kivy.base import EventLoop
from kivy.uix.screenmanager import ScreenManager
from project import MyApp, MainScreen, TitleScreen, RecipeScreen, ExitScreen

class TestMyApp(unittest.TestCase):

    def setUp(self):
        if not EventLoop.event_listeners:
            EventLoop.init()

        self.app = MyApp()
        self.app.build()
        self.app.root = ScreenManager()
        self.main_screen = MainScreen(name="main")
        self.title_screen = TitleScreen(name="title")
        self.recipe_screen = RecipeScreen(name="recipe")
        self.exit_screen = ExitScreen(name="exit")
        self.app.root.add_widget(self.main_screen)
        self.app.root.add_widget(self.title_screen)
        self.app.root.add_widget(self.recipe_screen)
        self.app.root.add_widget(self.exit_screen)
        self.app.root.current = "main"

    def test_bck_2_main_screen(self):
        self.assertEqual(self.app.root.current, "main")
        
    def test_switch_to_title(self):
        self.app.root.current = "title"
        self.assertEqual(self.app.root.current, "title")
    
    def test_go_to_recipe_screen(self):
        self.app.root.current = "recipe"
        self.assertEqual(self.app.root.current, "recipe")
    
    def test_go_to_exit_screen(self):
        self.app.root.current = "exit"
        self.assertEqual(self.app.root.current, "exit")


    def tearDown(self):
        self.app.stop()
        self.app = None
        self.main_screen = None

if __name__ == '__main__':
    unittest.main()
