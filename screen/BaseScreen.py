import logging
import time

from util.FileUtil import FileUtil
from util.Player import Player


class BaseScreen:
    def __init__(self, player: Player, signature: str) -> None:
        self.player = player
        self.signature = signature

    def get_class_name(self):
        return self.__class__.__name__

    def is_display(self, need_capture=True):
        logging.info("is_display " + self.get_class_name())
        try:
            pos = self.player.get_pos_click2(FileUtil.get_image_full_path(self.signature), need_capture=need_capture)
        except Exception as e:
            pos = self.player.get_pos_click2(FileUtil.get_image_full_path(self.signature), need_capture=need_capture)

        logging.info(pos)
        if pos:
            return True
        else:
            return False

    def wait_util_display(self, timeout=10):
        logging.info("wait_util_display " + self.get_class_name())
        logging.info(FileUtil.get_image_full_path(self.signature))
        self.player.wait_image(FileUtil.get_image_full_path(self.signature), timeout)

    #
    # def click_common_btn(self, need_capture=True):
    #     logging.info("click_common_btn " + self.get_class_name())
    #     common_btns: list[str] = ["data/common_btn_ok.png",
    #                               "data/common_btn_ok2.png",
    #                               "data/common_btn_open_all.png",
    #                               "data/common_btn_collect.png",
    #                               "data/common_btn_collect2.png",
    #                               "data/common_btn_retry.png",
    #                               "data/common_btn_ok3.png"
    #                               ]
    #
    #     if need_capture:
    #         self.player.screen_cap()
    #     for btnPath in common_btns:
    #         if self.player.is_contain_image(FileUtil.get_image_full_path(btnPath), need_capture=False):
    #             self.player.click_to_image(FileUtil.get_image_full_path(btnPath), need_capture=False)
    #             time.sleep(2)

    def click_next(self):
        self.player.click_to_image(FileUtil.get_image_full_path("data/common_next_btn.png"))
        time.sleep(2)

    def click_convert(self):
        self.player.click_to_image(FileUtil.get_image_full_path("data/common_convert_btn.png"))
        time.sleep(2)


    def hide_keyboard(self):
        self.player.click(214, 360)
        time.sleep(3)