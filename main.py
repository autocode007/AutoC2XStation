import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from screen.ConvertIDLELuca import ConvertIDLELuca
from util.ADB import ADB
from util.Constant import *
from util.License import check_license
from util.TelegramBot import TelegramBot
from util.TerraWallet import TerraWallet
from screen.Connect import Connect
from screen.ConvertLostCenturia import ConvertLostCenturia
from screen.ConvertChromaticSouls import ConvertChromaticSouls
from screen.Home import Home
from screen.RecoverWallet import RecoverWallet
from util import ExcelManager
from util.FileUtil import FileUtil

logging.basicConfig(
    level=int(logging.DEBUG),
    format="%(asctime)s [%(levelname)s] %(threadName)s %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

PACKAGE_NAME = "c2xstation.android"


def import_wallet(player, seed_phrase: str, gmail: str, nameC2x: str):
    logging.debug("import wallet:" +player.get_title())
    connect_screen = Connect(player)
    print(connect_screen.is_display())

    player.remountDevice()
    player.clear_app_data(PACKAGE_NAME)
    # player.push_app_data(PACKAGE_NAME, gmail)
    time.sleep(1)
    player.run_app(PACKAGE_NAME)
    connect_screen.wait_util_display()
    time.sleep(2)
    isHome = False
    try:
        isHome = player.is_contain_image(FileUtil.get_image_full_path("data/sig_home.png"))
    except Exception as ex:
        print(str(ex))
    if not isHome:
        connect_screen.go_to_recover_wallet()
        recover_wallet = RecoverWallet(player, nameC2x)
        recover_wallet.wait_util_display()
        recover_wallet.import_use_seed_phrase(seed_phrase)

def convert_dust_to_lct(player, seed_phrase):
    home_screen = Home(player)
    home_screen.goto_convert_lost_centuria()

    convert_lost_centuria_screen = ConvertLostCenturia(player)
    return convert_lost_centuria_screen.convert_dust_to_lct(seed_phrase)


def convert_dust_to_cst(player, seed_phrase, gmail, phone, password):
    home_screen = Home(player)
    home_screen.goto_convert_idle_luca()

    convert_idle_luca = ConvertIDLELuca(player)
    return convert_idle_luca.convert_mithril_to_cst(seed_phrase, gmail, phone, password)


def player_thread(player, seed_phrase, gmail, nameC2x, phone, password):
    terra_wallet = TerraWallet(seed_phrase)
    player.back_up_data()
    try:
        # adbplayer.screen_cap()
        logging.debug("player info: " + player.get_title())
        logging.debug("seed: " + seed_phrase)
        player.deleteAllApp()

        import_wallet(player, seed_phrase, gmail, nameC2x)
        result = convert_dust_to_cst(player, seed_phrase, gmail, phone, password)
        if result:
            player.screen_cap()
            TelegramBot.send_photo_message(player.get_title() + " - " + terra_wallet.get_address(),
                                           player.get_screenshot_file_path())
        # player.deleteAllApp()
        # connect_screen = Connect(player)
        # player.run_app(PACKAGE_NAME)
        # time.sleep(10)
        # player.pull_app_data(gmail)
    except Exception as e:
        # player.pull_app_data(gmail)
        player.screen_cap()
        logging.exception("Error " + str(e) + " - " + seed_phrase[0:10]+ " - "+player.get_title())

        TelegramBot.send_photo_message(player.get_title() + " - " + terra_wallet.get_address() + " Error:",
                                       player.get_screenshot_file_path()+" - "+str(e))

if __name__ == '__main__':
    # if not check_license():
    #     sys.exit(0)
    ListDataCheck = []
    try:
        ListDataCheck = ExcelManager.getListDataExcel("./AllProfilesC2X.xlsx", "Data")
    except Exception as e:
        print(str(e))

    list_device = []
    list_device_name = LIST_DEVICE.split("|")
    print(list_device_name)

    for device_name in list_device_name:
        adbplayer = ADB(device_name)
        list_device.append(adbplayer)
    print(len(list_device))

    thread_pool = ThreadPoolExecutor(max_workers=len(list_device))
    totalRun = len(ListDataCheck)
    index = 0
    for pos in range(totalRun):
        try:
            device_index = index % len(list_device)
            device = list_device[device_index]
            profile = ListDataCheck[pos]
            while str(profile.get("Phone")) == "nan":
                profile = ListDataCheck[pos]
                print("-------------------------------")
                print("Điền số điện thoại")
                print("STT: "+str(profile.get("STT")))
                print("Gmail: "+profile.get("Gmail"))
                print("STT: "+profile.get("Gmail"))
                print("Máy: "+device.get_title())
                time.sleep(5)
                try:
                    ListDataCheck = ExcelManager.getListDataExcel("./AllProfilesC2X.xlsx", "Data")
                except Exception as e:
                    print(str(e))
            phone = str(int(profile.get("Phone")))
            thread_pool.submit(player_thread, device, profile.get("Mnemonic"), profile.get("Gmail"), profile.get("NameC2X"),phone , profile.get("PasswordC2x"))

        except Exception as e:
            logging.error("Error " + str(e) + " - " + str(pos))

        index += 1
        pos += 1