from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import webbrowser as web
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


class MainMenu(BoxLayout):
    def __init__(self):
        super().__init__(orientation='vertical', spacing=5)
        logo = Label(text='Minesweeper [size=14]by zorzr[/size]', markup=True,
                     font_size='50px', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        basic = Button(text='Basic', size_hint=(None, None), size=(300, 70),
                       pos_hint={'center_x': 0.5, 'center_y': 0.5}, on_press=lambda _: gui.basic())
        inter = Button(text='Intermediate', size_hint=(None, None), size=(300, 70),
                       pos_hint={'center_x': 0.5, 'center_y': 0.5}, on_press=lambda _: gui.intermediate())
        expert = Button(text='Expert', size_hint=(None, None), size=(300, 70),
                        pos_hint={'center_x': 0.5, 'center_y': 0.5}, on_press=lambda _: gui.expert())
        custom = Button(text='Custom', size_hint=(None, None), size=(300, 70), on_press=lambda _: gui.soon(),
                        pos_hint={'center_x': 0.5, 'center_y': 0.5})

        bottom_box = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(300, 70),
                               pos_hint={'center_x': 0.5, 'center_y': 0.5}, spacing=3)
        cred = Button(text='Credits', on_press=lambda _: gui.credits())
        close = Button(text='Quit', on_press=lambda _: exit(0))

        bottom_box.add_widget(cred)
        bottom_box.add_widget(close)
        self.add_widget(logo)
        self.add_widget(Widget(size=(300, 10), size_hint=(None, None)))
        self.add_widget(basic)
        self.add_widget(inter)
        self.add_widget(expert)
        self.add_widget(custom)
        self.add_widget(bottom_box)
        self.add_widget(Widget(size=(300, 50), size_hint=(None, None)))


class GameField(BoxLayout):
    def __init__(self, rows, cols, bombs):
        super().__init__(orientation='horizontal', spacing=20, padding=[10, 10, 10, 0])
        self.grid = FieldGrid(rows, cols, bombs)
        self.r = rows
        self.c = cols
        self.b = bombs

        grid_anchor = AnchorLayout(anchor_x='left', anchor_y='top')
        buttons_anchor = AnchorLayout(anchor_x='right', anchor_y='top')
        buttons = BoxLayout(orientation='vertical', spacing=5, size_hint=(None, None), size=(100, 120))
        new_game = Button(text="New game", size_hint=(None, None), size=(100, 30), on_press=lambda _: self.new_game())
        menu = Button(text="Main menu", size_hint=(None, None), size=(100, 30), on_press=lambda _: gui.to_menu())
        mark = ToggleButton(text="Mark", size_hint=(None, None), size=(100, 30))
        mark.bind(state=lambda *_: self.change_mark())

        grid_anchor.add_widget(self.grid)
        buttons.add_widget(mark)
        buttons.add_widget(new_game)
        buttons.add_widget(menu)
        buttons.add_widget(Widget())
        buttons_anchor.add_widget(buttons)

        self.add_widget(grid_anchor)
        self.add_widget(buttons_anchor)

    def change_mark(self):
        self.grid.mark = not self.grid.mark

    def new_game(self):
        self.grid.board = Board(self.r, self.c, self.b)
        self.grid.reload_board()
        self.grid.over = False


class FieldGrid(GridLayout):
    def __init__(self, rows, cols, bombs):
        super().__init__(cols=cols, pos_hint={'center_x': 0.5, 'center_y': 0.7},
                         size=(cols*22, rows*22), size_hint=(None, None))
        self.board = Board(rows, cols, bombs)
        self.over = False
        self.mark = False

        for i in range(rows*cols):
            tile = TileWidget(i)
            self.add_widget(tile)

    def tile_pressed(self, index):
        if self.over:
            return

        tile = self.board.tiles[index]
        n_tiles = self.board.rows * self.board.cols

        if self.mark:
            if not tile.covered:
                return

            self.board.mark_tile(index)
            if tile.marked:
                self.children[n_tiles-1-index].change_image("mark")
            else:
                self.children[n_tiles-1-index].change_image("cov")

            if self.board.status() == 1:
                self.over = True
        else:
            if tile.marked:
                return
            self.board.expose_tile(index)
            widget = self.children[n_tiles-1-index]

            if self.board.status() == 0 and tile.value != 0:
                widget.change_image(str(tile.value))
            elif self.board.status() == 0 and tile.value == 0:
                self.reload_board()
            elif self.board.status() == -1:
                widget.change_image("bomb")
                self.over = True

    def reload_board(self):
        n_tiles = self.board.rows*self.board.cols
        for i in range(n_tiles):
            w = self.children[n_tiles-1-i]
            t = self.board.tiles[i]

            if t.covered and t.marked:
                w.change_image("mark")
            elif t.covered and not t.marked:
                w.change_image("cov")
            else:
                w.change_image(str(t.value))


class TileWidget(AnchorLayout):
    def __init__(self, tile_index):
        super().__init__(anchor_x='center', anchor_y='center')
        self.image = TileButton(source=images["cov"], size_hint=(None, None), size=(20, 20))
        self.add_widget(self.image)
        self.index = tile_index

    def handle_press(self):
        self.parent.tile_pressed(self.index)

    def change_image(self, status):
        self.image.source = images[status]


class TileButton(ButtonBehavior, Image):
    def on_press(self):
        grid = self.parent.parent
        mark = grid.mark
        if self.last_touch.button == 'right':
            grid.mark = True
        self.parent.handle_press()
        if self.last_touch.button == 'right':
            grid.mark = mark


class InterfaceManager(BoxLayout):
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        self.menu = MainMenu()
        self.add_widget(self.menu)

    def to_menu(self):
        Window.size = (800, 600)
        self.clear_widgets()
        self.add_widget(self.menu)

    def to_minefield(self, r, c, b):
        self.clear_widgets()
        self.add_widget(GameField(r, c, b))

    def basic(self):
        Window.size = (350, 220)
        self.to_minefield(9, 9, 10)

    def intermediate(self):
        Window.size = (500, 370)
        self.to_minefield(16, 16, 40)

    def expert(self):
        Window.size = (800, 370)
        self.to_minefield(16, 30, 99)

    @staticmethod
    def soon():
        content = Image(source="images/soon.jpg")
        popup = Popup(title="Soon", content=content, size_hint=(None, None), size=(230, 200))
        popup.open()

    @staticmethod
    def credits():
        buttons = GridLayout(cols=3, padding=[20, 0, 20, 0])
        content = BoxLayout(orientation='vertical', spacing=5)
        credit = Label(text="\nGame design:                       zorzr\n"
                            "UI design:                             zorzr")
        thanks = Label(text="Special thanks to StackOverflow")
        github = Button(text="Website", size_hint=(None, None), size=(100, 40))
        close = Button(text="Close", size_hint=(None, None), size=(100, 40))

        buttons.add_widget(github)
        buttons.add_widget(Widget())
        buttons.add_widget(close)
        content.add_widget(credit)
        content.add_widget(thanks)
        content.add_widget(buttons)
        popup = Popup(title="Credits", content=content, size_hint=(None, None), size=(300, 200))

        close.bind(on_press=popup.dismiss)
        github.bind(on_press=lambda *_: web.open_new("https://github.com/zorzr"))
        popup.open()


class MinesweeperApp(App):
    def build(self):
        return gui


if __name__ == "__main__":
    gui = InterfaceManager()
    MinesweeperApp().run()
