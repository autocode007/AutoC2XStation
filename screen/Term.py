import time

from util.FileUtil import FileUtil
from util.Player import Player
from screen.BaseScreen import BaseScreen


class Term(BaseScreen):
    def __init__(self, player: Player) -> None:
        super().__init__(player, "data/sig_term.png")

    def agree_all(self):
        self.player.click_to_image(FileUtil.get_image_full_path("data/term_agree_all.png"))
        time.sleep(2)
        self.player.click_to_image(FileUtil.get_image_full_path("data/common_confirm_btn.png"))
        time.sleep(2)
        self.player.click_to_image(FileUtil.get_image_full_path("data/term_ok_btn.png"))
        time.sleep(3)