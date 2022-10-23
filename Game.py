import random
from time import time
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

class WindowManager(ScreenManager):
    pass

class MenuWindow(Screen):
    def go_to_game(self):
        self.parent.current = "game_window"
        self.manager.screens[1].init_game()

class GameWindow(Screen):
    game_label = ObjectProperty(None)
    fields = ObjectProperty(None)

    # Starts a new game
    def init_game(self):
        self.game_label.text = "Welcome to memory game."
        self.random_assignement()
        self.first_shown = None
        self.previous_bad_pair = None
        self.guessed_fields = []
        self.game_start = time()
        for i in range(16):
            button = self.get_button(i)
            button.text = ""
            button.disabled = False

    # Assigns values to the fields
    def random_assignement(self):
        self.assignment = {}
        remaining_indices = list(range(16))
        for i in range(8):
            value1 = random.choice(remaining_indices)
            remaining_indices.remove(value1)
            self.assignment[value1] = i
            value2 = random.choice(remaining_indices)
            remaining_indices.remove(value2)
            self.assignment[value2] = i

    def show_button(self, i):
        button = self.get_button(i)
        if button.disabled:
            return
        button.text = str(self.assignment[i])

        if self.previous_bad_pair is not None:
            first_bad, second_bad = self.previous_bad_pair
            if first_bad != i:
                first_bad_button = self.get_button(first_bad)
                first_bad_button.text = ""
            if second_bad != i:
                second_bad_button = self.get_button(second_bad)
                second_bad_button.text = ""
            self.previous_bad_pair = None

        if self.first_shown is None:
            self.first_shown = i

        elif self.first_shown != i:
            first_value = self.assignment[self.first_shown]
            second_value = self.assignment[i]

            if first_value == second_value:
                previous_button = self.get_button(self.first_shown)
                previous_button.disabled = True
                button.disabled = True
                self.guessed_fields += [self.first_shown, i]

            else:
                self.previous_bad_pair = (self.first_shown, i)
            self.first_shown = None

        if len(self.guessed_fields) == 16:
            self.win_game_info()

    def get_button(self, i):
        return self.fields.children[15 - i]

    def win_game_info(self):
        game_end = time()
        self.game_label.text = f"\nCongratulations, you won in {int(game_end - self.game_start)} seconds!!!"

kv = Builder.load_file("Game.kv")

class MemeoryGameApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MemeoryGameApp().run()
