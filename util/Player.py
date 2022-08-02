import random
from abc import abstractmethod
from email.mime import image
import subprocess
import os
import time
import cv2
import numpy as np
import logging
from util.FileUtil import FileUtil

PATH_LDP = '"' + "D:\LDPlayer\LDPlayer4.0\ldconsole.exe" + '"'


class Keys:
    HOME = '3'
    BACK = '4'
    CALL = '5'
    END_CALL = '6'
    VOL_UP = '24'
    VOL_DOWN = '25'
    POWER = '26'
    CAMERA = '27'
    BROWSER = '64'
    ENTER = '66'
    BACKSPACE = '67'
    PHONEBOOK = '207'
    LIGHT_UP = '220'
    LIGHT_DOWN = '221'
    CUT = '277'
    COPY = '278'
    PATSE = '279'


class Player():
    def __init__(self, path: str, index: int = None, name: str = None) -> None:
        if index != None:
            self.index = str(index)
            self.path = path
            self.name = None
        elif name:
            self.name = name
            self.path = path
            self.index = None

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def quit(self):
        pass

    @abstractmethod
    def run_app(self, package: str):
        pass

    @abstractmethod
    def is_app_running(self, package: str):
        pass

    @abstractmethod
    def is_running(self):
        pass

    @abstractmethod
    def click(self, x: int, y: int):
        pass

    @abstractmethod
    def is_contain_image(self, image_path: str, need_capture=True):
        pass

    @abstractmethod
    def click_to_image(self, image: str, random_target: bool = False, need_capture=True):
        pass

    @abstractmethod
    def get_pos_click2(self, img_path: str, multi: bool = False, need_capture=True):
        pass

    @abstractmethod
    def wait_image(self, image: str, timeout: int = 10):
        pass

    @abstractmethod
    def send_text(self, text: str):
        pass

    @abstractmethod
    def send_key_event(self, key: str):
        pass

    @abstractmethod
    def screen_cap(self):
        pass

    @abstractmethod
    def back_up_data(self):
        pass

    def get_screenshot_file_path(self):
        if self.name:
            return FileUtil.get_image_full_path(f"images-screencap/{self.name}.png")
        else:
            return FileUtil.get_image_full_path(f"images-screencap/index{self.index}.png")

    def get_title(self):
        if self.name:
            return self.name
        else:
            return "index-" + str(self.index)

    @classmethod
    def get_pos_click(
            cls,
            cap: str,
            obj: str,
            center: bool = True,
            multi: bool = False,
            threshold: float = 0.7,
            eps: float = 0.05,
            show: bool = False
    ) -> list:
        img_base = cv2.imread(cap)
        img_find = cv2.imread(obj)
        width = img_find.shape[1]
        height = img_find.shape[0]
        result = cv2.matchTemplate(img_base, img_find, cv2.TM_CCOEFF_NORMED)
        pos = []
        if multi:
            y_loc, x_loc = np.where(result >= threshold)
            rectangles = []
            for x, y in zip(x_loc, y_loc):
                rectangles.append([int(x), int(y), int(width), int(height)])
                rectangles.append([int(x), int(y), int(width), int(height)])
            for x, y, w, h in cv2.groupRectangles(rectangles, 1, eps)[0]:
                cv2.rectangle(img_base, (x, y), (x + w, y + h), (0, 0, 255), 2)
                if center:
                    pos.append((x + w // 2, y + h // 2))
                else:
                    pos.append((x, y))
        else:
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            logging.debug(max_val)
            if max_val > threshold:
                cv2.rectangle(
                    img_base, max_loc, (max_loc[0] + width, max_loc[1] + height), (0, 0, 255), 2)
                if center:
                    pos.append((max_loc[0] + width // 2,
                                max_loc[1] + height // 2))
                else:
                    pos.append(max_loc)
        if show:
            cv2.imshow("show", img_base)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return pos
