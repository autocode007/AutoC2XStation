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
        super().__init__(player, "data/c2x_idle_luca_sign.png")

    def open_tab_convert(self):
        self.player.click(530, 2500)
        time.sleep(3)

    def open_idle_luca(self):
        self.player.click_to_image(FileUtil.get_image_full_path("data/c2x_idle_luca_sign.png"))
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

    def convert_mithril_to_cst(self, seed_phrase, gmail, phone, password):
        listLocationCharacter = ["2281"]
        for character in listLocationCharacter:
            if not self.process_convert(character, False, gmail, phone, password):
                self.process_convert(character, True, gmail, phone, password)
        return True

    def deleteAllApp(self):
        self.player.send_key_event("187")
        time.sleep(2)
        for i in range(3):
            self.player.click(705, 63)
            time.sleep(2)
        for i in range(3):
            self.player.send_key_event("4")
            time.sleep(1)
    def process_convert(self, character, is_over_token, gmail: str, phone: str, password: str):
        # Verphone
        time.sleep(8)
        if not self.player.click_to_image(FileUtil.get_image_full_path("data/c2x_brave_continue.png")):
            self.player.click(706, 1093)
        time.sleep(2)
        if not self.player.click_to_image(FileUtil.get_image_full_path("data/c2x_brave_continue_1.png")):
            self.player.click(708, 1218)
        time.sleep(3)
        if self.player.is_contain_image(FileUtil.get_image_full_path("data/c2x_idle_luca_open_ver_phone.png")):
            #Click open + 1
            self.player.click_to_image(FileUtil.get_image_full_path("data/c2x_idle_luca_open_ver_phone.png"))
            time.sleep(2)
            for xx in range(3):
                self.player.swipe(629, 2269, 653, 521)
                time.sleep(2)
            for xx in range(3):
                if not self.player.click_to_image(FileUtil.get_image_full_path("data/c2x_idle_luca_vietname.png")):
                    break
                self.player.swipe(629, 2169, 663, 510)
                time.sleep(2)

            self.player.click(900, 1616)
            time.sleep(2)
            self.player.send_text(phone)
            time.sleep(2)
            self.hide_keyboard()
            if not self.player.click_to_image(FileUtil.get_image_full_path("data/c2x_idle_luca_oke.png")):
                self.player.click(1058, 1919)
            time.sleep(10)
            self.player.wait_image(FileUtil.get_image_full_path("data/c2x_idle_luca_logo_hive.png"), 200)
            if self.player.is_contain_image(FileUtil.get_image_full_path("data/c2x_idle_luca_logo_hive.png")):
                if not self.player.click_to_image(FileUtil.get_image_full_path("data/c2x_idle_luca_login_hive.png")):
                    # Gmail
                    time.sleep(5)
                    self.player.click(555, 1200)
                    time.sleep(3)
                    self.player.send_text(gmail)
                    self.hide_keyboard()
                    time.sleep(2)
                    # Password
                    self.player.click(1175, 1437)
                    time.sleep(3)
                    self.player.send_text(password)
                    self.hide_keyboard()
                    time.sleep(2)
                    if not self.player.click_to_image(
                            FileUtil.get_image_full_path("data/c2x_idle_login.png")):
                        self.player.click(1235, 2068)
                    time.sleep(10)
                    if self.player.is_contain_image(FileUtil.get_image_full_path("data/c2x_idle_luca_hive_login_error.png")):
                        print("error")
                    self.player.wait_image(FileUtil.get_image_full_path("data/c2x_idle_luca_sign.png"), 5)
        else:
            pass

        self.open_tab_convert()
        self.open_idle_luca()

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
            self.player.click(726, 2357)
            if not is_over_token:
                return False
        except Exception as ex:
            self.player.screen_cap()
            TelegramBot.send_photo_message(self.player.get_title() + " - " + terra_wallet.get_address() + " Success: ",
                                           self.player.get_screenshot_file_path())
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

