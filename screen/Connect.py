from util.FileUtil import FileUtil
from util.Player import Player
from screen.BaseScreen import BaseScreen


class Connect(BaseScreen):
    def __init__(self, player: Player) -> None:
        super().__init__(player, "data/sig_connect.png")

    def go_to_recover_wallet(self):
        self.player.click_to_image(FileUtil.get_image_full_path("data/connect-recover-wallet-btn.png"))

