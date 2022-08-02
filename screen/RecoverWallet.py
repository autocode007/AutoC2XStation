import time

from util.Constant import WALLET_PASSWORD, WALLET_NAME
from util.FileUtil import FileUtil
from util.Player import Player
from screen.BaseScreen import BaseScreen


class RecoverWallet(BaseScreen):
    def __init__(self, player: Player) -> None:
        super().__init__(player, "data/sig_recover_wallet.png")

    def click_explore(self):
        self.player.click_to_image(FileUtil.get_image_full_path("data/recover_explore_btn.png"))
        time.sleep(2)


    def import_use_seed_phrase(self,phrase):
        if not self.is_display():
            raise Exception("Go to recover screen first!")

        self.player.click_to_image(FileUtil.get_image_full_path("data/recover_wallet_use_seed_phrase.png"))
        time.sleep(3)
        #fill seed phrase
        self.player.click(712, 832)
        time.sleep(2)
        self.player.send_text(phrase)
        time.sleep(2)
        self.hide_keyboard()
        time.sleep(2)
        self.click_next()

        #fill name and password
        self.player.click(712,703) #name
        time.sleep(2)
        self.player.send_text(WALLET_NAME)
        time.sleep(2)

        self.player.click(712, 1048)  # pass1
        time.sleep(2)
        self.player.send_text(WALLET_PASSWORD)
        time.sleep(2)

        self.player.click(712, 1378)  # pass2
        time.sleep(2)
        self.player.send_text(WALLET_PASSWORD)
        time.sleep(2)
        self.hide_keyboard()
        self.click_next()
        time.sleep(12)
        self.player.click(636, 688)  # pass2
        time.sleep(2)
        self.click_explore()

