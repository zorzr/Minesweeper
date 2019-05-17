from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from game import Board

images = {
    "cov": "images/covered.png",
    "mark": "images/marked.png",
    "bomb": "images/bomb.png",
    "0": "images/0.png",
    "1": "images/1.png",
    "2": "images/2.png",
    "3": "images/3.png",
    "4": "images/4.png",
    "5": "images/5.png",
    "6": "images/6.png",
    "7": "images/7.png",
    "8": "images/8.png",
}


class ImageButton(ButtonBehavior, Image):
    def on_press(self):
        mark = app.mark
        if self.last_touch.button == 'right':
            app.mark = True
        self.parent.handle_press()
        if self.last_touch.button == 'right':
            app.mark = mark


class TileWidget(BoxLayout):
    def __init__(self, tile_index, **kwargs):
        super().__init__(**kwargs)
        self.index = tile_index
        self.image = ImageButton(source=images["cov"], pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                 size_hint=(None, None), size=(20, 20))
        self.add_widget(self.image)

    def handle_press(self):
        self.parent.tile_pressed(self.index)

    def change_image(self, status):
        self.image.source = images[status]


class FieldWidget(GridLayout):
    def __init__(self):
        super().__init__(cols=10, size_hint=(None, None), size=(300, 300),
                         pos_hint={'center_x': 0.5, 'center_y': 0.5})

        self.over = False
        for i in range(100):
            tile = TileWidget(i)
            self.add_widget(tile)

    def tile_pressed(self, index):
        if self.over:
            return

        tile = app.board.tiles[index]
        if app.mark:
            if not tile.covered:
                return

            app.board.mark_tile(index)
            if tile.marked:
                self.children[99-index].change_image("mark")
            else:
                self.children[99-index].change_image("cov")

            if app.board.status() == 1:
                self.over = True
        else:
            if tile.marked:
                return
            app.board.expose_tile(index)
            widget = self.children[99-index]

            if app.board.status() == 0 and tile.value != 0:
                widget.change_image(str(tile.value))
            elif app.board.status() == 0 and tile.value == 0:
                self.reload_board()
            elif app.board.status() == -1:
                widget.change_image("bomb")
                self.over = True

    def reload_board(self):
        for i in range(100):
            w = self.children[99-i]
            t = app.board.tiles[i]

            if t.covered and t.marked:
                w.change_image("mark")
            elif t.covered and not t.marked:
                w.change_image("cov")
            else:
                w.change_image(str(t.value))


class MineApp(App):
    mark = False
    board = Board(10, 10, 16)
    grid = FieldWidget()

    def build(self):
        Window.size = (400, 300)
        box = BoxLayout(orientation="horizontal", spacing=20)

        buttons = BoxLayout(orientation="vertical", spacing=10)
        mark = ToggleButton(text="Mark", size_hint=(None, None), size=(70, 30))
        close = Button(text="Close", size_hint=(None, None), size=(70, 30))
        new_game = Button(text="New game", size_hint=(None, None), size=(80, 30))
        mark.bind(state=self.set_mark_state)
        close.bind(on_press=lambda _: exit(0))
        new_game.bind(on_press=lambda _: self.new_game())

        buttons.add_widget(mark)
        buttons.add_widget(close)
        buttons.add_widget(new_game)
        buttons.add_widget(Widget())
        box.add_widget(self.grid)
        box.add_widget(buttons)
        return box

    def set_mark_state(self, *_):
        self.mark = not self.mark

    def new_game(self):
        self.board = Board(10, 10, 16)
        self.grid.reload_board()
        self.grid.over = False


if __name__ == "__main__":
    app = MineApp()
    app.run()
