import logging
import os
import random
from pathlib import Path

from ppadb.client import Client
from ppadb.device import Device

from util.Player import Player


class ADB(Player):
    client: Client = None

    def __init__(self, name: str = None) -> None:
        self.device: Device = None
        self.name = name
        if not ADB.client:
            ADB.client = Client(host="127.0.0.1", port=5037)
            listDevices = ADB.client.devices()
        self.device = ADB.client.device(self.name)
        self.device.create_connection()

    def run(self):
        pass

    def quit(self):
        pass

    def run_app(self, package: str):
        logging.info("----------Run app--------- " + package)
        self.device.shell("monkey -p " + package + " -c android.intent.category.LAUNCHER 1")

    def is_app_running(self, package: str):
        result = self.device.shell("dumpsys activity lru | grep TOP")
        if package in result:
            return True
        else:
            return False

    def is_running(self):
        pass

    def click(self, x: int, y: int):
        self.device.input_tap(str(x), str(y))

    def is_contain_image(self, image_path: str, need_capture=True):
        pos = self.get_pos_click2(image_path, need_capture=need_capture)
        logging.debug("is_contain_image " + str(pos) + " - " + image_path)
        if pos:
            return True
        return False

    def click_to_image(self, image: str, random_target: bool = False, need_capture=True):
        logging.info("click to image " + image + "--------------------")
        pos = self.get_pos_click2(image, multi=random_target, need_capture=need_capture)
        target_index = 0
        logging.info(pos)
        if random_target:
            target_index = random.randint(0, len(pos) - 1)

        if pos:
            x, y = pos[target_index]
            self.click(x, y)

    def get_pos_click2(self, img_path: str, multi: bool = False, need_capture=True):
        logging.info("GET pos click2 - " + img_path)
        if need_capture:
            self.screen_cap()
        pos = Player.get_pos_click(os.path.abspath(
            f"images-screencap/{self.name}.png"), img_path, multi=multi)
        return pos

    def wait_image(self, image: str, timeout: int = 10):
        self.screen_cap()
        while not Player.get_pos_click(os.path.abspath(
                f"images-screencap/{self.name}.png"), image) and timeout > 0:
            self.screen_cap()
            timeout -= 1
        if timeout < 1:
            raise TimeoutError("Can't find image on screen")
        else:
            return True

    def send_text(self, text: str):
        logging.debug("send text "+self.get_title()+" - "+text)
        self.device.input_text(text)

    def send_key_event(self, key: str):
        self.device.input_keyevent(keycode=key)

    def screen_cap(self):
        result = self.device.screencap()
        screen_shot_path = os.path.abspath("./images-screencap")
        Path(screen_shot_path).mkdir(parents=True, exist_ok=True)

        output_path = screen_shot_path + "/" + self.name + ".png"
        with open(output_path, "wb") as fp:
            fp.write(result)

    def clear_app_data(self, package: str):
        self.device.clear(package)
