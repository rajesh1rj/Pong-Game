from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from random import randint


class Ball(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class GamePaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, game_ball):
        if self.collide_widget(game_ball):
            game_ball.velocity_x *= -1


class Game(Widget):
    game_ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self):
        self.game_ball.velocity = Vector(5, 0).rotate(randint(0, 360))

    def update(self, dt):
        self.game_ball.move()

        # bounce off top and bottom
        if (self.game_ball.y < 0) or (self.game_ball.y > self.height - 50):
            self.game_ball.velocity_y *= -1

        # bounce off left
        if self.game_ball.x < 0:
            self.game_ball.velocity_x *= -1
            self.player1.score += 1

        # right
        if self.game_ball.x > self.width - 50:
            self.game_ball.velocity_x *= -1
            self.player2.score += 1

        self.player1.bounce_ball(self.game_ball)
        self.player2.bounce_ball(self.game_ball)

    def on_touch_move(self, touch):
        if touch.x < self.width / 1 / 4:
            self.player1.center_y = touch.y
        if touch.x > self.width * 3 / 4:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = Game()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 50.0)
        return game


PongApp().run()
