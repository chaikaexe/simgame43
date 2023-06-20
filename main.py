import arcade
import random

CIRCLE_COORDS = [(200, 125), (100, 275), (200, 425), (400, 425), (500, 275), (400, 125)]
LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H"]
IS_VS_BOT = False


class Circle:
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.color = arcade.color.BLACK
        self.connections_count = 0
        self.max_connections = None
        self.letter = letter

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, 15, self.color)
        arcade.draw_text(self.letter, self.x - 25, self.y - 25, arcade.color.BLACK, 14)


class Connection:
    def __init__(self, circle1, circle2, color):
        self.circle1 = circle1
        self.circle2 = circle2
        self.color = color
        self.circle1.connections_count += 1
        self.circle2.connections_count += 1

    def draw(self):
        arcade.draw_line(self.circle1.x, self.circle1.y, self.circle2.x, self.circle2.y, self.color, 5)


class Bot:
    def __init__(self, circles, player_color):
        self.circles = circles
        self.player_color = player_color

    def make_move(self):
        available_moves = []
        for i in range(len(self.circles)):
            circle = self.circles[i]
            if circle.connections_count < circle.max_connections:
                available_moves.append(i)

        # Выберите случайный доступный ход или реализуйте свою стратегию выбора хода

        if available_moves:
            selected_circle = random.choice(available_moves)
            return selected_circle

        return None


class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Игра Сим", self.window.width / 2, self.window.height / 2 + 50,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text("Играть", self.window.width / 2, self.window.height / 2 - 50,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Правила", self.window.width / 2 + 12, self.window.height / 2 - 95,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Выход", self.window.width / 2, self.window.height / 2 - 140,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("F - переключение режима окна", self.window.width / 2, self.window.height / 2 - 200,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (
                    self.window.width / 2 - 50 <= x <= self.window.width / 2 + 50
                    and self.window.height / 2 - 70 <= y <= self.window.height / 2 - 30
            ):
                selectmode_view = SelectMode()
                self.window.show_view(selectmode_view)
            elif (
                    self.window.width / 2 - 50 <= x <= self.window.width / 2 + 50
                    and self.window.height / 2 - 120 <= y <= self.window.height / 2 - 80
            ):
                rules_view = RulesView()
                self.window.show_view(rules_view)
            elif (
                    self.window.width / 2 - 50 <= x <= self.window.width / 2 + 50
                    and self.window.height / 2 - 170 <= y <= self.window.height / 2 - 130
            ):
                arcade.close_window()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F:
            self.window.set_fullscreen(not self.window.fullscreen)
            self.on_draw()


class SelectMode(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Выберите режим игры", self.window.width / 2, self.window.height / 2 + 50,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text("Игрок против игрока", self.window.width / 2, self.window.height / 2 - 50,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Игрок против бота", self.window.width / 2, self.window.height / 2 - 100,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        global IS_VS_BOT
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (
                self.window.width / 2 - 135 <= x <= self.window.width / 2 + 135
                and self.window.height / 2 - 70 <= y <= self.window.height / 2 - 30
            ):
                IS_VS_BOT = False
                levelselect_view = LevelSelect()
                self.window.show_view(levelselect_view)
            elif (
                self.window.width / 2 - 120 <= x <= self.window.width / 2 + 120
                and self.window.height / 2 - 120 <= y <= self.window.height / 2 - 80
            ):
                IS_VS_BOT = True
                levelselect_view = LevelSelect()
                self.window.show_view(levelselect_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)


class LevelSelect(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Выберите уровень", self.window.width / 2, self.window.height / 2 + 50,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text("6 кругов", self.window.width / 2, self.window.height / 2 - 50,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("7 кругов", self.window.width / 2, self.window.height / 2 - 100,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("8 кругов", self.window.width / 2, self.window.height / 2 - 150,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (
                self.window.width / 2 - 50 <= x <= self.window.width / 2 + 50
                and self.window.height / 2 - 70 <= y <= self.window.height / 2 - 30
            ):
                self.window.game_view = Sim()
                self.window.game_view.setup(6)
                self.window.show_view(self.window.game_view)
            elif (
                self.window.width / 2 - 50 <= x <= self.window.width / 2 + 50
                and self.window.height / 2 - 120 <= y <= self.window.height / 2 - 80
            ):
                self.window.game_view = Sim()
                self.window.game_view.setup(7)
                self.window.show_view(self.window.game_view)
            elif (
                self.window.width / 2 - 50 <= x <= self.window.width / 2 + 50
                and self.window.height / 2 - 170 <= y <= self.window.height / 2 - 130
            ):
                self.window.game_view = Sim()
                self.window.game_view.setup(8)
                self.window.show_view(self.window.game_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)


class RulesView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        text = "На игровом поле расположено несколько точек («вершин»), в данном случае их 6\n\n" \
               "Игроки (два пользователя) по очереди проводят линии, соединяющие две ещё не соединённые вершины (цвет линий пользователей — красный и синий).\n\n" \
               "Проигрывает игрок, после хода которого образуется треугольник со сторонами проведёнными этим игроком (треугольники, образовавшиеся в результате пересечения линий не учитываются).\n\n" \
               "Чтобы сделать ход:\n" \
               "С помощью мыши выберите нужную вершину, кликнув левой кнопкой мыши по ней, далее выберите вторую вершину тем же способом.\n\n" \
               "esc - выйти в главное меню"
        if self.window.fullscreen:
            arcade.draw_text(text, self.window.width / 2, self.window.height / 2 + 150, arcade.color.BLACK,
                             font_size=22, anchor_x="center", align="center", width=self.window.width - 20)
        else:
            arcade.draw_text(text, self.window.width / 2, self.window.height / 2 + 150, arcade.color.BLACK,
                             font_size=14, anchor_x="center", align="center", width=self.window.width - 20)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)


class Sim(arcade.View):
    def __init__(self):
        super().__init__()
        self.circles = []
        self.connections = []
        self.selected_circle = None
        self.player = arcade.color.RED
        self.used_connections = []
        self.game_over = False
        self.bot = None
        self.last_player = arcade.color.RED
        self.winner_message = None

    def setup(self, num_circles):
        arcade.set_background_color(arcade.color.WHITE)
        circle_coords = CIRCLE_COORDS
        if num_circles == 6:
            circle_coords = CIRCLE_COORDS
            max_connections = 5
        if num_circles == 7:
            circle_coords = [(300, 400), (470, 320), (520, 170), (400, 60), (200, 60), (80, 170), (130, 320)]
            max_connections = 6
        if num_circles == 8:
            circle_coords = [(300, 400), (430, 330), (490, 220), (430, 110), (300, 40), (170, 110), (110, 220), (170, 330)]
            max_connections = 7
        if self.window.fullscreen:
            if num_circles == 6:
                circle_coords = [(600, 338), (300, 619), (600, 900), (1200, 900), (1500, 619), (1200, 338)]
            if num_circles == 7:
                circle_coords = [(900, 1000), (1410, 800), (1560, 425), (1200, 150), (600, 150), (240, 425), (390, 800)]
            if num_circles == 8:
                circle_coords = [(900, 1000), (1296, 825), (1476, 550), (1296, 275), (900, 220), (504, 275), (396, 550), (504, 825)]
        self.circles = [Circle(*coords, letter) for coords, letter in zip(circle_coords, LETTERS)]
        for circle in self.circles:
            circle.max_connections = max_connections
        self.bot = Bot(self.circles, self.player)

    def make_bot_move(self):
        if IS_VS_BOT:
            available_connections = []
            for i in range(len(self.circles)):
                for j in range(i + 1, len(self.circles)):
                    if (i, j) not in self.used_connections and (j, i) not in self.used_connections:
                        available_connections.append((i, j))
            if available_connections:
                circle_index1, circle_index2 = random.choice(available_connections)
                self.connections.append(
                    Connection(self.circles[circle_index1], self.circles[circle_index2], self.player))
                self.check_game_over()
                self.player = arcade.color.BLUE if self.player == arcade.color.RED else arcade.color.RED
                self.used_connections.append((circle_index1, circle_index2))

    def on_draw(self):
        arcade.start_render()
        for circle in self.circles:
            circle.draw()
        for connection in self.connections:
            connection.draw()
        if self.selected_circle is not None:
            arcade.draw_circle_outline(
                self.circles[self.selected_circle].x,
                self.circles[self.selected_circle].y,
                15,
                self.player,
                5,
            )
        if self.game_over:
            arcade.start_render()
            size = self.window.get_size()
            arcade.draw_text(self.winner_message, size[0] / 2, size[1] / 2, arcade.color.BLACK, font_size=40, anchor_x="center")
            arcade.draw_text("esc - выйти в главное меню", self.window.width / 2, self.window.height / 2 - 100,
                             arcade.color.BLACK, font_size=20, anchor_x="center")
        else:
            player_message = "Ходит красный игрок" if self.player == arcade.color.RED else "Ходит синий игрок"
            arcade.draw_text(player_message, 10, self.window.height - 20, arcade.color.BLACK, font_size=16)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for i in range(len(self.circles)):
                circle = self.circles[i]
                distance = ((x - circle.x) ** 2 + (y - circle.y) ** 2) ** 0.5
                if distance <= 15 and circle.connections_count < circle.max_connections:
                    if self.selected_circle is None:
                        self.selected_circle = i
                    elif self.selected_circle == i:
                        self.selected_circle = None
                    else:
                        if (self.selected_circle, i) not in self.used_connections and (
                                i, self.selected_circle
                        ) not in self.used_connections:
                            self.connections.append(
                                Connection(self.circles[self.selected_circle], self.circles[i], self.player))
                            self.player = arcade.color.BLUE if self.player == arcade.color.RED else arcade.color.RED
                            self.used_connections.append((self.selected_circle, i))
                            self.selected_circle = None
                            self.make_bot_move()
                            self.check_game_over()
                            break

    def check_game_over(self):
        for i in range(len(self.circles)):
            for j in range(i + 1, len(self.circles)):
                for k in range(j + 1, len(self.circles)):
                    circle1 = self.circles[i]
                    circle2 = self.circles[j]
                    circle3 = self.circles[k]
                    connections = [
                        conn for conn in self.connections
                        if (conn.circle1 in [circle1, circle2, circle3] and conn.circle2 in [circle1, circle2, circle3])]
                    if len(connections) == 3:
                        colors = [conn.color for conn in connections]
                        if colors == [arcade.color.RED] * 3:
                            self.winner_message = "Победил синий игрок"
                            self.game_over = True
                        if colors == [arcade.color.BLUE] * 3:
                            self.winner_message = "Победил красный игрок"
                            self.game_over = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)


def main():
    window = arcade.Window(640, 480, "Игра Сим")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
