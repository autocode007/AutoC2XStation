import logging
import os
import random
import subprocess

from util.Player import Player
from util.Players import Players

PATH_LDP = '"' + "D:\LDPlayer\LDPlayer4.0\ldconsole.exe" + '"'


class LDPlayers(Players):
    def __init__(self, path: str = PATH_LDP) -> None:
        sp = subprocess.Popen(path, shell=True, stdout=subprocess.PIPE)
        if "dnplayer Command Line Management Interface" not in sp.stdout.readline().decode():
            raise SystemError("Ldconsole not found")
        self.path = path
        subprocess.Popen(f"""{path} adb --index 0 --command "start-server" """)

    def find_by_index(self, index: int):
        sp = subprocess.Popen(self.path + " list",
                              shell=True, stdout=subprocess.PIPE)
        count = -1
        while sp.stdout.readline():
            count += 1
        if -1 < index <= count:
            return LDPlayer(path=self.path, index=index)
        else:
            raise ValueError("LDPlayer is not found")

    def find_by_name(self, name: str):
        sp = subprocess.Popen(self.path + " list",
                              shell=True, stdout=subprocess.PIPE)
        while line := sp.stdout.readline().strip():
            line = line.decode('cp850')
            if name == line:
                return LDPlayer(path=self.path, name=name)
        raise ValueError("LDPlayer is not found " + str(name))

    def show(self):
        logging.debug(subprocess.Popen(self.path + " list", shell=True))

    def create(self, name: str):
        logging.debug(subprocess.Popen(self.path + " add --name " + name, shell=True))

    def delete_by_name(self, name: str):
        logging.debug(subprocess.Popen(self.path + " remove --name " + name, shell=True))

    def delete_by_index(self, index: int):
        logging.debug(subprocess.Popen(self.path + " remove --index " + index, shell=True))

    def copy(self, name: str, fromName: str):
        logging.debug(subprocess.Popen(self.path + " copy --name " +
                                       name + " --from " + fromName, shell=True))

    def quitall(self):
        logging.debug(subprocess.Popen(self.path + " quitall", shell=True))


class LDPlayer(Player):
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
                                           " launch --name " + self.name, shell=True))
        elif self.index:
            logging.debug(subprocess.Popen(self.path +
                                           " launch --index " + self.index, shell=True))

    def quit(self):
        logging.info("Quit " + self.name)
        if self.name:
            logging.debug(subprocess.Popen(self.path +
                                           " quit --name " + self.name, shell=True))
        elif self.index:
            logging.debug(subprocess.Popen(self.path +
                                           " quit --index " + self.index, shell=True))

    def run_app(self, package: str):
        logging.info("Run app " + package)

        if self.name:
            logging.info(subprocess.Popen(self.path +
                                          " runapp --name " + self.name + " --packagename " + package, shell=True))
        elif self.index:
            logging.info(subprocess.Popen(self.path +
                                          " runapp --index " + self.index + " --packagename " + package, shell=True))

    def is_app_running(self, package: str):
        p = None
        command = ""
        if self.name:
            command = self.path + " adb --name " + self.name + " --command \"shell pidof " + package + "\""
        elif self.index:
            command = self.path + " adb --index " + self.index + " --command \"shell pidof " + package + "\""

        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd_result, err) = p.communicate()
        p_status = p.wait()
        logging.info(p_status)
        logging.info(cmd_result)
        if cmd_result and cmd_result.strip():
            return True
        else:
            return False

    def is_running(self):
        cmd_result = "stop"
        p = None
        if self.name:
            p = subprocess.Popen(self.path +
                                 " isrunning --name " + self.name, stdout=subprocess.PIPE, shell=True)
        elif self.index:
            p = subprocess.Popen(self.path +
                                 " isrunning --index " + self.index, stdout=subprocess.PIPE, shell=True)

        (cmd_result, err) = p.communicate()
        p.wait()
        is_running = "running" in str(cmd_result)
        return is_running

    def click(self, x: int, y: int):
        logging.info("click - " + str(x) + " - " + str(y))
        if self.name:
            subprocess.Popen(self.path + " adb --name " + '"' + self.name +
                             '"' + " --command " + '"' + "shell input tap " + str(x) + " " + str(y) + '"')
        elif self.index:
            subprocess.Popen(self.path + " adb --index " + self.index +
                             " --command " + '"' + "shell input tap " + str(x) + " " + str(y) + '"')

    def is_contain_image(self, image_path: str, need_capture=True):
        pos = self.get_pos_click2(image_path, need_capture=need_capture)
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
                subprocess.Popen(self.path + " adb --name " + '"' + self.name +
                                 '"' + " --command " + '"' + "shell input tap " + str(x) + " " + str(y) + '"')
            elif self.index:
                x, y = pos[target_index]
                subprocess.Popen(self.path + " adb --index " + self.index +
                                 " --command " + '"' + "shell input tap " + str(x) + " " + str(y) + '"')
            return True
        return False
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
        try:
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
        except Exception as ex:
            print("Error")
            return False

    def send_text(self, text: str):
        if self.name:
            subprocess.Popen(self.path + " adb --name " + '"' + self.name +
                             '"' + " --command " + '"' + "shell input text \'" + text + '\'"')
        elif self.index:
            subprocess.Popen(self.path + " adb --index " + self.index +
                             " --command " + '"' + "shell input text \'" + text + '\'"')

    def send_key_event(self, key: str):
        if self.name:
            subprocess.Popen(self.path + " adb --name " + '"' + self.name +
                             '"' + " --command " + '"' + "shell input keyevent " + key + '"')
        elif self.index:
            subprocess.Popen(self.path + " adb --index " + self.index +
                             " --command " + '"' + "shell input keyevent " + key + '"')

    def swipe(self, x1, y1, x2, y2):
        if self.name:
            subprocess.Popen(self.path + " adb --name " + '"' + self.name +
                             '"' + " --command " + '"' + "shell input touchscreen swipe " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + ' 750 "')
        elif self.index:
            subprocess.Popen(self.path + " adb --index " + self.index +
                             '"' + " --command " + '"' + "shell input touchscreen swipe " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + ' 750 "')

    def screen_cap(self):

        logging.info("Capture screen")
        imgPath = ""
        if self.name:
            imgPath = os.path.abspath("./images-screencap/") + "/" + self.name + ".png"
            os.makedirs(os.path.abspath("../images-screencap"), exist_ok=True)
            command = f"""{self.path} adb --name "{self.name}" --command "shell screencap -p /sdcard/{self.name}.png" """
            logging.debug(command)
            subprocess.Popen(command, shell=True).communicate()
            pull_command = f"""{self.path} adb --name "{self.name}" --command "pull /sdcard/{self.name}.png ./images-screencap" """
            subprocess \
                .Popen(pull_command) \
                .communicate()

        elif self.index:
            imgPath = os.path.abspath("./images-screencap/") + "/" + self.index + ".png"
            os.makedirs(os.path.abspath("../images-screencap"), exist_ok=True)
            subprocess.Popen(
                f"""{self.path} adb --index {self.index} --command "shell screencap -p /sdcard/index{self.index}.png" """,
                shell=True).communicate()

            subprocess.Popen(
                f"""{self.path} adb --index {self.index} --command "pull /sdcard/index{self.index}.png {os.path.abspath("../images-screencap")}" """,
                shell=True).communicate()

        statfile = os.stat(imgPath)
        filesize = statfile.st_size
        if filesize == 0:
            os.remove(imgPath)
            self.screen_cap()

    def back_up_data(self):
        subprocess.Popen(self.path + " adb backup -f all -all -apk -nosystem ")
        self.click(1083, 2480)
