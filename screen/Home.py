import time

from util.FileUtil import FileUtil
from util.Player import Player
from screen.BaseScreen import BaseScreen
from screen.Term import Term


class Home(BaseScreen):
    def __init__(self, player: Player) -> None:
        super().__init__(player, "data/sig_home.png")

    def open_tab_convert(self):
        self.player.click(530, 2500)
        time.sleep(3)

    def open_lost_centuria(self):
        self.player.click_to_image(FileUtil.get_image_full_path("data/convert_lost_centuria_sig.png"))

    def open_chromatic_souls(self):
        self.player.click_to_image(FileUtil.get_image_full_path("data/convert_chromatic_souls_sig.png"))

    def goto_convert_chromatic_souls(self):
        term_screen = Term(self.player)
        self.open_tab_convert()
        if term_screen.is_display():
            term_screen.agree_all()
        self.open_chromatic_souls()

    def open_idle_luca(self):
        self.player.click_to_image(FileUtil.get_image_full_path("data/c2x_idle_luca_sign.png"))

    def goto_convert_idle_luca(self):
        term_screen = Term(self.player)
        self.open_tab_convert()
        if term_screen.is_display():
            term_screen.agree_all()
        self.open_idle_luca()

    def goto_convert_lost_centuria(self):
        term_screen = Term(self.player)
        self.open_tab_convert()
        if term_screen.is_display():
            term_screen.agree_all()
        self.open_lost_centuria()

