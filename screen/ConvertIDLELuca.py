import logging
import time

from util.Constant import WALLET_PASSWORD
from util.FileUtil import FileUtil
from util.Player import Player, Keys
from util.TelegramBot import TelegramBot
from util.TerraWallet import TerraWallet
from screen.BaseScreen import BaseScreen


class ConvertIDLELuca(BaseScreen):
    def __init__(self, player: Player) -> None:
        super().__init__(player, "data/chromatic_souls_sig.png")

    def open_tab_convert(self):
        self.player.click(530, 2500)
        time.sleep(3)

    def open_chromatic_souls(self):
        self.player.click_to_image(FileUtil.get_image_full_path("data/convert_chromatic_souls_sig.png"))
        time.sleep(10)

    def open_select_character(self):
        self.player.click_to_image(FileUtil.get_image_full_path("data/sig_select_character1.png"))
        time.sleep(2)

    def click_select_character(self, locationCharacter):
        self.player.wait_image(FileUtil.get_image_full_path("data/sig_select_character.png"), 60)
        self.player.click(1229, int(locationCharacter))
        print("++++++++++++++++")
        time.sleep(3)

    def click_next(self):
        self.player.click_to_image(FileUtil.get_image_full_path("data/common_next_btn.png"))
        time.sleep(2)

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

    def convert_mithril_to_cst(self, seed_phrase):
        listLocationCharacter = ["1653", "1865", "2065", "2281"]
        for character in listLocationCharacter:
            if not self.process_convert(character, False):
                self.process_convert(character, True)
        return True

    def process_convert(self, character, is_over_token):
        self.open_tab_convert()
        self.open_chromatic_souls()

        # self.wait_util_display()
        self.open_select_character()

        self.click_select_character(character)
        time.sleep(2)
        self.player.click(730, 2359)
        self.click_game_token()
        self.click_game_token()
        self.click_game_token()
        self.click_swap()
        if not is_over_token:
            self.click_available()
        else:
            self.player.click(1150, 915)
            self.player.send_text('4000')
            time.sleep(2)
            self.hide_keyboard()
            time.sleep(2)
        try:
            if self.player.is_contain_image(FileUtil.get_image_full_path("data/convert_not_enough.png")):
                # terra_wallet = TerraWallet(seed_phrase)
                # TelegramBot.send_photo_message(self.player.get_title() + " - " + terra_wallet.get_address() + " - not enough ",
                #                                self.player.get_screenshot_file_path())
                # # back then click new character
                self.player.send_key_event(Keys.BACK)
                time.sleep(2)
                return True
        except Exception as ex1:
            logging.error(ex1)
        self.click_next()
        self.confirm_password()
        self.hide_keyboard()
        time.sleep(2)
        self.click_convert()

        try:
            self.player.wait_image(FileUtil.get_image_full_path("data/exceeded_maximum_request_per_day.png"), 60)
            self.player.send_key_event(Keys.BACK)
            if not is_over_token:
                return False
        except Exception as ex:
            self.player.screen_cap()
            TelegramBot.send_photo_message(self.player.get_title() + " - " + terra_wallet.get_address() + " Success: ",
                                           self.player.get_screenshot_file_path())
            self.player.send_key_event(Keys.BACK)
            time.sleep(2)
        return True
