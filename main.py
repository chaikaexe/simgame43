import arcade

# Определение констант
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CIRCLE_RADIUS = 15
CIRCLE_SPACING = 80
CIRCLE_COORDS = [(200, 125), (100, 275), (200, 425), (400, 425), (500, 275), (400, 125)]
LETTERS = ["A", "B", "C", "D", "E", "F"]


# Определение класса для кружочков
class Circle:
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.color = arcade.color.BLACK
        self.connections_count = 0
        self.max_connections = 5
        self.letter = letter

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, CIRCLE_RADIUS, self.color)
        arcade.draw_text(self.letter, self.x - 25, self.y - 25, arcade.color.BLACK, 14)


# Определение класса для соединений
class Connection:
    def __init__(self, circle1, circle2, color):
        self.circle1 = circle1
        self.circle2 = circle2
        self.color = color
        self.circle1.connections_count += 1
        self.circle2.connections_count += 1

    def draw(self):
        arcade.draw_line(self.circle1.x, self.circle1.y, self.circle2.x, self.circle2.y, self.color, 5)


class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Игра Сим", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text("Играть", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Выход", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        if SCREEN_WIDTH/2 - 50 <= x <= SCREEN_WIDTH/2 + 50 and SCREEN_HEIGHT/2 - 70 <= y <= SCREEN_HEIGHT/2 - 30:
            game_view = Sim()
            game_view.setup()
            self.window.show_view(game_view)
        elif SCREEN_WIDTH/2 - 50 <= x <= SCREEN_WIDTH/2 + 50 and SCREEN_HEIGHT/2 - 120 <= y <= SCREEN_HEIGHT/2 - 80:
            arcade.close_window()


# Определение класса игры
class Sim(arcade.View):
    def __init__(self):
        super().__init__()
        self.circles = []
        self.connections = []
        self.selected_circle = None
        self.player = arcade.color.RED
        self.used_connections = []
        self.game_over = False

    def setup(self):
        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        arcade.set_window(self.window)
        arcade.set_background_color(arcade.color.WHITE)
        self.circles = [Circle(*coords, letter) for coords, letter in zip(CIRCLE_COORDS, LETTERS)]

    def on_draw(self):
        arcade.start_render()
        for circle in self.circles:
            circle.draw()
        for connection in self.connections:
            connection.draw()
        if self.selected_circle is not None:
            # нельзя убрать is not None т.к. учитываем случай когда self.selected_circle равно 0
            arcade.draw_circle_outline(self.circles[self.selected_circle].x, self.circles[self.selected_circle].y,
                                       CIRCLE_RADIUS, self.player, 5)
        if self.game_over:
            arcade.start_render()
            size = self.window.get_size()
            winner_color = arcade.color.BLUE if self.player == arcade.color.RED else arcade.color.RED
            winner_message = "Победил синий игрок" if winner_color == arcade.color.RED else "Победил красный игрок"
            arcade.draw_text(winner_message, size[0] / 2, size[1] / 2, arcade.color.BLACK, font_size=40,
                             anchor_x="center")
            arcade.draw_text("esc - выйти в главное меню", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100,
                             arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for i in range(len(self.circles)):
                circle = self.circles[i]
                distance = ((x - circle.x) ** 2 + (y - circle.y) ** 2) ** 0.5
                if distance <= CIRCLE_RADIUS and circle.connections_count < 5:
                    if self.selected_circle is None:
                        self.selected_circle = i
                    elif self.selected_circle == i:
                        self.selected_circle = None
                    else:
                        if (self.selected_circle, i) not in self.used_connections and (i, self.selected_circle) not in self.used_connections:
                            self.connections.append(Connection(self.circles[self.selected_circle], self.circles[i], self.player))
                            self.player = arcade.color.BLUE if self.player == arcade.color.RED else arcade.color.RED
                            self.used_connections.append((self.selected_circle, i))
                            self.selected_circle = None
                            self.check_game_over()

    def check_game_over(self):
        for i in range(len(self.circles)):
            for j in range(i + 1, len(self.circles)):
                for k in range(j + 1, len(self.circles)):
                    circle1 = self.circles[i]
                    circle2 = self.circles[j]
                    circle3 = self.circles[k]
                    connections = [
                        conn for conn in self.connections
                        if (conn.circle1 in [circle1, circle2, circle3] and conn.circle2 in [circle1, circle2, circle3])
                    ]
                    if len(connections) == 3:
                        colors = [conn.color for conn in connections]
                        if colors == [arcade.color.RED] * 3:
                            self.game_over = True
                        elif colors == [arcade.color.BLUE] * 3:
                            self.game_over = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Игра Сим")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
