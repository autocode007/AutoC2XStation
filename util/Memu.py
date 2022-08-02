import logging
import os
import random
import subprocess

from util.FileUtil import FileUtil
from util.Player import Player
from util.Players import Players

PATH_LDP = '"' + "D:\Program Files\Microvirt\MEmu\memuc.exe" + '"'


class Memus(Players):
    def __init__(self, path: str = PATH_LDP) -> None:
        path = '"' + path + '"'
        sp = subprocess.Popen(path, shell=True, stdout=subprocess.PIPE)
        if "MEmu Command Line Tool" not in sp.stdout.readline().decode():
            raise SystemError("Memu not found")
        self.path = path
        subprocess.Popen(f"""{path} -i 0 adb "start-server" """)

    def find_by_index(self, index: int):
        sp = subprocess.Popen(self.path + " listvms",
                              shell=True, stdout=subprocess.PIPE)
        count = -1
        while sp.stdout.readline():
            count += 1
        if -1 < index <= count:
            return MemuPlayer(path=self.path, index=index)
        else:
            raise ValueError("LDPlayer is not found")

    def find_by_name(self, name: str):
        sp = subprocess.Popen(self.path + " listvms",
                              shell=True, stdout=subprocess.PIPE)
        print(sp)
        while line := sp.stdout.readline().strip():
            line = line.decode('cp850')
            print(line)
            player_info = line.split(",")
            if name == player_info[1]:
                return MemuPlayer(path=self.path, name=name)
        raise ValueError("LDPlayer is not found")

    def show(self):
        logging.debug(subprocess.Popen(self.path + " listvms", shell=True))

    def quitall(self):
        logging.debug(subprocess.Popen(self.path + " stopall", shell=True))


class MemuPlayer(Player):
    def __init__(self, path: str, index: int = None, name: str = None) -> None:
        if index != None:
            self.index = str(index)
            self.path = path
            self.name = None
        elif name:
            self.name = name
            self.path = path
            self.index = None

    def run(self):
        if self.name:
            logging.debug(subprocess.Popen(self.path +
                                           " start  -t -n " + self.name, shell=True))
        elif self.index:
            logging.debug(subprocess.Popen(self.path +
                                           " start -t -i " + self.index, shell=True))

    def quit(self):

        if self.name:
            logging.info("------------------Quit----------------" + self.name)
            logging.debug(subprocess.Popen(self.path +
                                           " stop -n " + self.name, shell=True))
        elif self.index:
            logging.info("------------------Quit----------------" + self.index)
            logging.debug(subprocess.Popen(self.path +
                                           " stop -i " + self.index, shell=True))

    def run_app(self, package: str):
        logging.info("----------Run app--------- " + package)
        if self.name:
            logging.debug(subprocess.Popen(self.path +
                                           " startapp -n " + self.name + " " + package, shell=True))
        elif self.index:
            logging.debug(subprocess.Popen(self.path +
                                           " startapp -i " + self.index + " " + package, shell=True))

    def is_app_running(self, package: str):
        self.screen_cap()
        if self.is_contain_image(FileUtil.get_image_full_path("data/play_store_logo.png"), need_capture=False):
            logging.info("Memu is staying at android_home")
            return False

        p = None
        command = ""
        if self.name:
            command = self.path + " -n " + self.name + " adb \"shell pidof " + package + "\""
        elif self.index:
            command = self.path + " -i " + self.index + " adb \"shell pidof " + package + "\""

        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd_result, err) = p.communicate()
        p_status = p.wait()
        logging.debug(str(cmd_result) + " - lsof ")
        lines = cmd_result.splitlines()
        lines = list(filter(None, lines))

        if len(lines) < 2:
            return False
        else:
            return True

    def is_running(self):
        cmd_result = "stop"
        p = None
        if self.name:
            p = subprocess.Popen(self.path +
                                 " isvmrunning -n " + self.name, stdout=subprocess.PIPE, shell=True)
        elif self.index:
            p = subprocess.Popen(self.path +
                                 " isvmrunning -i " + self.index, stdout=subprocess.PIPE, shell=True)

        (cmd_result, err) = p.communicate()
        p.wait()
        is_running = not "Not Running" in str(cmd_result)
        return is_running

    def click(self, x: int, y: int):
        logging.info("click - " + str(x) + " - " + str(y))
        if self.name:
            subprocess.Popen(self.path + " -n " + '"' + self.name +
                             '"' + " adb " + '"' + "shell input tap " + str(x) + " " + str(y) + '"')
        elif self.index:
            subprocess.Popen(self.path + " -i " + self.index +
                             " adb " + '"' + "shell input tap " + str(x) + " " + str(y) + '"')

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
            if self.name:
                x, y = pos[target_index]
                subprocess.Popen(self.path + " -n " + '"' + self.name +
                                 '"' + " adb " + '"' + "shell input tap " + str(x) + " " + str(y) + '"')
            elif self.index:
                x, y = pos[target_index]
                subprocess.Popen(self.path + " -i " + self.index +
                                 " adb " + '"' + "shell input tap " + str(x) + " " + str(y) + '"')

    def get_pos_click2(self, img_path: str, multi: bool = False, need_capture=True):
        logging.info("GET pos click2 - " + img_path)
        if need_capture:
            self.screen_cap()
        if self.name:
            pos = Player.get_pos_click(os.path.abspath(
                f"images-screencap/{self.name}.png"), img_path, multi=multi)
            return pos
        elif self.index:
            pos = Player.get_pos_click(os.path.abspath(
                f"images-screencap/index{self.index}.png"), img_path, multi=multi)
            return pos

    def wait_image(self, image: str, timeout: int = 10):
        self.screen_cap()
        if self.name:
            while not Player.get_pos_click(os.path.abspath(
                    f"images-screencap/{self.name}.png"), image) and timeout > 0:
                self.screen_cap()
                timeout -= 1
            if timeout < 1:
                raise TimeoutError("Can't find image on screen")
            else:
                return True

        elif self.index:
            while not Player.get_pos_click(os.path.abspath(
                    f"images-screencap/index{self.index}.png"), image) and timeout > 0:
                self.screen_cap()
                timeout -= 1
            if timeout < 1:
                raise TimeoutError("Can't find image on screen")
            else:
                return True

    def send_text(self, text: str):
        if self.name:
            subprocess.Popen(self.path + " -n " + '"' + self.name +
                             '"' + " adb " + '"' + "shell input text \'" + text + '\'"')
        elif self.index:
            subprocess.Popen(self.path + " -i " + self.index +
                             " adb " + '"' + "shell input text \'" + text + '\'"')

    def send_key_event(self, key: str):
        if self.name:
            subprocess.Popen(self.path + " -n " + '"' + self.name +
                             '"' + " adb " + '"' + "shell input keyevent " + key + '"')
        elif self.index:
            subprocess.Popen(self.path + " -i " + self.index +
                             " adb " + '"' + "shell input keyevent " + key + '"')

    def screen_cap(self):

        logging.debug("Capture screen")
        imgPath = ""
        if self.name:
            imgPath = os.path.abspath("./images-screencap/") + "/" + self.name + ".png"
            os.makedirs(os.path.abspath("../images-screencap"), exist_ok=True)
            command = f"""{self.path} -n "{self.name}" adb "shell screencap -p /sdcard/{self.name}.png" """
            logging.debug(command)
            subprocess.Popen(command, shell=True).communicate()
            pull_command = f"""{self.path} -n "{self.name}" adb "pull /sdcard/{self.name}.png ./images-screencap" """
            subprocess \
                .Popen(pull_command) \
                .communicate()

        elif self.index:
            imgPath = os.path.abspath("./images-screencap/") + "/index" + self.index + ".png"
            os.makedirs(os.path.abspath("./images-screencap"), exist_ok=True)
            subprocess.Popen(
                f"""{self.path} -i {self.index} adb "shell screencap -p /sdcard/index{self.index}.png" """,
                shell=True).communicate()

            subprocess.Popen(
                f"""{self.path} -i {self.index} adb "pull /sdcard/index{self.index}.png {os.path.abspath("./images-screencap")}" """,
                shell=True).communicate()

        statfile = os.stat(imgPath)
        filesize = statfile.st_size
        if filesize == 0:
            os.remove(imgPath)
            self.screen_cap()
