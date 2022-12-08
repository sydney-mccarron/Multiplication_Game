import arcade
from arcade import load_texture
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane
import random
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Zombie (arcade.Sprite):

    def update(self):
        ## bounce off sides
        if self.left <= 0:
            self.change_x = 0
        elif self.right >= SCREEN_WIDTH:
            self.change_x *= -1

        super().update()

class Mygame(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_GRAY)

        self.text = ""
        self.moveit = False
        self.level = 1
        self.numbercorrect = 0
        self.newquestion = []
        self.score = 0
        self.score_text = " "
        self.firstquestion = ""


        ## Questions and Answers

        self.level_one_questions = ["1 * 1", "2 * 1", "3 * 1", "4 * 1", "5 * 1", "6 * 1", "7 * 1", "8 * 1", "9 * 1", "10 * 1"]
        self.level_one_answers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.current_question = self.level_one_questions
        self.current_answers = self.level_one_answers

        self.level_two_questions = ["2 * 2", "2 * 3", "2 * 4", "2 * 5", "2 * 6", "2 * 7", "2 * 8", "2 * 9", "2 * 10", "4 *10"]
        self.level_two_answers = ["4", "6", "8", "10", "12", "14", "16", "18", "20", "40"]

        self.level_three_questions = ["3 * 3", "3 * 4", "3 * 5", "3 * 6", "3 * 7", "4 * 5", "4 * 6", "4 * 7", "4 * 8", "9 * 8"]
        self.level_three_answers = ["9", "12", "15", "18", "21", "20", "24", "28", "32", "72"]

        self.level_four_questions = ["4 * 4", "5 * 6", "6 * 6", "7 * 7", "8 * 8", "9 * 9", "10 * 10", "12 * 10", "11 * 11", "12 * 12"]
        self.level_four_answers = ["16", "30", "36", "49", "64", "81", "100", "120", "121", "144"]

        #Backup for when all the previous list is removed
        self.backup_question1 = self.level_one_questions[:]
        self.backup_answers1 = self.level_one_answers[:]


        self.backup_question2 = self.level_two_questions[:]
        self.backup_answers2 = self.level_two_answers[:]

        self.backup_question3 = self.level_three_questions[:]
        self.backup_answers3 = self.level_three_answers[:]

        self.backup_question4 = self.level_four_questions[:]
        self.backup_answers4 = self.level_four_answers[:]





    ##Questions for each level
    def setup(self):
        self.my_zombie = Zombie(":resources:images/animated_characters/zombie/zombie_walk5.png")
        self.my_zombie.center_x = 35
        self.my_zombie.center_y = SCREEN_HEIGHT // 2
        self.my_zombie.scale = 0.75

        ##Where backup questions are added in
        if len(self.current_question) == 1:
            if self.level == 1:
                self.level_one_questions = self.backup_question1[:]
                self.level_one_answers = self.backup_answers1[:]
            elif self.level == 2:
                self.level_two_questions = self.backup_question2[:]
                self.level_two_answers = self.backup_answers2[:]
            elif self.level == 3:
                self.level_three_questions = self.backup_question3[:]
                self.level_three_answers = self.backup_answers3[:]
            elif self.level == 4:
                self.level_four_questions = self.backup_question4[:]
                self.level_four_answers = self.backup_answers4[:]
        elif self.firstquestion == "":
            print("first")
        else:
            self.current_question.remove(self.firstquestion)
            self.current_answers.remove(self.answer)
        if self.level == 1:
            self.current_question = self.level_one_questions
            self.current_answers = self.level_one_answers
        elif self.level == 2:
            self.current_question = self.level_two_questions
            self.current_answers = self.level_two_answers
        elif self.level == 3:
            self.current_question = self.level_three_questions
            self.current_answers = self.level_three_answers
        elif self.level == 4:
            self.current_question = self.level_four_questions
            self.current_answers = self.level_four_answers


        print(self.level)
        ##Random assignment of questions
        question_index = random.randint(0, len(self.current_question)-1)
        self.firstquestion = self.current_question[question_index]
        self.answer = self.current_answers[question_index]

        # print(self.current_question)

        self.manager = UIManager()
        self.manager.enable()
        ## Create Text Area
        bg_tex = load_texture(":resources:gui_basic_assets/window/grey_panel.png")
        text_area = UITextArea(x=340,
                               y=410,
                               width=200,
                               height=100,
                               text=self.firstquestion,
                               text_color=(0, 0, 0, 255))

        self.manager.add(
            UITexturePane(
                text_area.with_space_around(right=20),
                tex=bg_tex,
                padding=(10, 10, 10, 10)))

        ##Text input area
        self.input_area = UIInputText(x=340, y=300, width=200, height=50, text="")
        self.manager.add(
            UITexturePane(
                #UIInputText(x=340, y=200, width=200, height=50, text=""),
                self.input_area,
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            ))

        ##Text on screen
        self.manager.add(
            UIInputText(x=340, y=210, width=200, height=50, text=self.text),
        )

        self.manager.add(
            UIInputText(x=340, y=160, width=200, height=50, text= self.score_text),
        )
        ##Buttons
        # Create a BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Next Question and End Game buttons
        reload_button = arcade.gui.UIFlatButton(text="Next Question", width=200)
        self.v_box.add(reload_button.with_space_around(bottom=20))

        reload_button.on_click = self.on_click_start

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


    ##Telling the user if their answer is correct
    def on_click_start(self, event):
        print("My Start:", event)
        self.text = self.input_area.text
        if self.text == self.answer:
            print("correct")
            self.text = "You are right"
            self.numbercorrect += 1
            self.score += 1
            print(self.score)
            self.score_text = "Score: " + str(self.score)
            if self.numbercorrect == 3 and self.level < 4:
                self.level += 1
                self.moveit = True
                self.numbercorrect = 0
            elif self.numbercorrect == 3 and self.level == 4:
                End_game = EndingView()
                self.window.show_view(End_game)
        else:
            self.text = " Try Again"
        self.clear()
        self.setup()

    ##Zombie Sprite
    def sprite_character(self):
        self.my_zombie = Zombie(":resources:images/animated_characters/zombie/zombie_walk5.png")
        self.my_zombie.center_x = 25
        self.my_zombie.center_y = SCREEN_HEIGHT // 2
        self.my_zombie.scale = 0.5

    ##Moving Zombie
    def update(self, delta_time):
        if self.moveit:
            self.my_zombie.change_x = 1
            self.moveit = False
        self.my_zombie.update()
        super().update(delta_time)

    def on_click_end(self, event):
        print("My Start:", event)
        end_view = EndingView()
        self.window.show_view(end_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()
        self.my_zombie.draw()

##Ending screen
class EndingView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLUEBERRY)
        self.background = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text("You Won! ", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        arcade.draw_text("Click to Exit Game", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
       arcade.exit()


