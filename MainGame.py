import arcade
from mygame import Mygame
from arcade import load_texture
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

LOREM_IPSUM = (
    "Welcome to Math Multiples game! You maybe wondering How do I play this game? Well here is how!\n"
    "\n"
    "A multiplication problem will pop up on your screen in the larger box. You will then enter your answer to the problem into the smaller box by using the numbers on your keyboard.\n"
    "\n"
    "Once you have typed the answer to the problem click the Next Question button.\n" 
    "\n" 
    "If your answer is correct you will earn a point. If your answer is incorrect you will not earn a point.\n"
    "\n" 
    "When you get 3 problems correct a Zombie will run aross the page. This shows that you have beat the level. \n"
    "\n"
    "Once your score hits 12 the game will end.\n"
    "\n"
    "Once you are ready to start the game press the START GAME button. \n"

)

class InstructionView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
        self.background = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text("Math Multiples", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Ready to learn!? ", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = MyWindow()
        game_view.setup()
        self.window.show_view(game_view)


class MyWindow(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_SEA_GREEN)

        self.text = ""

    ##Instructional screen
    def setup(self):
        self.manager = UIManager()
        self.manager.enable()
        self.level = "level 1"
        ## Create Text Area
        bg_tex = load_texture(":resources:gui_basic_assets/window/grey_panel.png")
        text_area = UITextArea(x=100,
                               y=200,
                               width=200,
                               height=300,
                               text=LOREM_IPSUM,
                               text_color=(0, 0, 0, 255))

        self.manager.add(
            UITexturePane(
                text_area.with_space_around(right=20),
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            )
        )


        ##Buttons
        # Create a BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        reload_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(reload_button.with_space_around(bottom=20))

        reload_button.on_click = self.on_click_reload

        end_button = arcade.gui.UIFlatButton(text="End Game ", width=200)
        self.v_box.add(end_button.with_space_around(bottom=20))

        end_button.on_click = self.on_click_end

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="bottom",
                child=self.v_box)
        )

    def on_click_reload(self, event):
        print("My Start:", event)
        start_game = Mygame()
        start_game.setup()
        self.window.show_view(start_game)


    def on_click_end(self, event):
        print("My Start:", event)
        end_view = EndingView()
        self.window.show_view(end_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()

##End game screen
class EndingView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLUEBERRY)
        self.background = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text("End of Game ", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        arcade.draw_text("Click to Exit Game", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    ##Leave game
    def on_mouse_press(self, _x, _y, _button, _modifiers):
       arcade.exit()


# window = MyWindow()
# arcade.run()
window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "GUI")
instruction_view = InstructionView()
window.show_view(instruction_view)
arcade.run()