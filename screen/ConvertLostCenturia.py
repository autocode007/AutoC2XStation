import time

from util.Constant import WALLET_PASSWORD
from util.FileUtil import FileUtil
from util.Player import Player
from util.TelegramBot import TelegramBot
from util.TerraWallet import TerraWallet
from screen.BaseScreen import BaseScreen


class ConvertLostCenturia(BaseScreen):
    def __init__(self, player: Player) -> None:
        super().__init__(player, "data/lost_centuria_sig.png")

    def open_tab_convert(self):
        self.player.click(530, 2500)
        time.sleep(3)

    def open_lost_centuria(self):
        self.player.click_to_image(FileUtil.get_image_full_path("data/convert_lost_centuria_sig.png"))

    def click_game_token(self):
        self.player.click(525, 551)
        time.sleep(2)

    def click_swap(self):
        self.player.click(720, 1140)
        time.sleep(2)

    def click_available(self):
        self.player.click(1300, 775)
        time.sleep(10)

    def confirm_password(self):
        self.player.click(700, 700)
        self.player.send_text(WALLET_PASSWORD)
        time.sleep(2)

    def click_next(self):
        self.player.click(742, 2500)
        time.sleep(2)

    def convert_dust_to_lct(self, seed_phrase):
        self.open_tab_convert()
        self.open_lost_centuria()

        self.wait_util_display()
        self.click_game_token()
        self.click_game_token()
        self.click_game_token()
        self.click_swap()
        self.click_available()

        if self.player.is_contain_image(FileUtil.get_image_full_path("data/convert_not_enough.png")):
            terra_wallet = TerraWallet(seed_phrase)
            TelegramBot.send_photo_message(self.player.get_title() + " - " + terra_wallet.get_address() + " - not enough ",
                                           self.player.get_screenshot_file_path())
            return False

        self.click_next()
        self.confirm_password()
        self.hide_keyboard()
        time.sleep(2)
        self.click_convert()

        self.player.wait_image(FileUtil.get_image_full_path("data/convert_success.png"), 20)

        self.player.screen_cap()

        return True
