import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor

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

logging.basicConfig(
    level=int(logging.DEBUG),
    format="%(asctime)s [%(levelname)s] %(threadName)s %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

PACKAGE_NAME = "c2xstation.android"


def import_wallet(player, seed_phrase: str):
    logging.debug("import wallet:" +player.get_title())
    connect_screen = Connect(player)
    recover_wallet = RecoverWallet(player)
    print(connect_screen.is_display())
    player.clear_app_data(PACKAGE_NAME)
    player.run_app(PACKAGE_NAME)
    connect_screen.wait_util_display()
    time.sleep(2)
    connect_screen.go_to_recover_wallet()

    recover_wallet.wait_util_display()
    recover_wallet.import_use_seed_phrase(seed_phrase)


def convert_dust_to_lct(player, seed_phrase):
    home_screen = Home(player)
    home_screen.goto_convert_lost_centuria()

    convert_lost_centuria_screen = ConvertLostCenturia(player)
    return convert_lost_centuria_screen.convert_dust_to_lct(seed_phrase)


def convert_dust_to_cst(player, seed_phrase):
    home_screen = Home(player)
    home_screen.goto_convert_chromatic_souls()

    convert_chromatic_souls_screen = ConvertChromaticSouls(player)
    return convert_chromatic_souls_screen.convert_mithril_to_cst(seed_phrase)


def player_thread(player, seed_phrase):
    terra_wallet = TerraWallet(seed_phrase)
    player.back_up_data()
    try:
        # adbplayer.screen_cap()
        logging.debug("player info: " + player.get_title())
        logging.debug("seed: " + seed_phrase)
        import_wallet(player, seed_phrase)
        # result = convert_dust_to_lct(player, seed_phrase)
        result = convert_dust_to_cst(player, seed_phrase)
        if result:
            player.screen_cap()
            TelegramBot.send_photo_message(player.get_title() + " - " + terra_wallet.get_address(),
                                           player.get_screenshot_file_path())
    except Exception as e:
        player.screen_cap()
        logging.exception("Error " + str(e) + " - " + seed_phrase[0:10]+ " - "+player.get_title())

        TelegramBot.send_photo_message(player.get_title() + " - " + terra_wallet.get_address() + " Error:",
                                       player.get_screenshot_file_path()+" - "+str(e))


if __name__ == '__main__':
    if not check_license():
        sys.exit(0)

    list_seed = []
    with open(SEED_PATH) as file:
        list_seed = file.readlines()
        list_seed = [line.rstrip() for line in list_seed]

    list_device = []
    list_device_name = LIST_DEVICE.split("|")
    print(list_device_name)

    for device_name in list_device_name:
        adbplayer = ADB(device_name)
        list_device.append(adbplayer)
    print(len(list_device))

    thread_pool = ThreadPoolExecutor(max_workers=len(list_device))
    index = 0
    for seed_phrase in list_seed:
        try:
            device_index = index % len(list_device)
            device = list_device[device_index]
            thread_pool.submit(player_thread, device, seed_phrase)
        except Exception as e:
            logging.error("Error " + str(e) + " - " + seed_phrase[0:10])

        index += 1

# import logging
# import sys
# import time
# from concurrent.futures import ThreadPoolExecutor
#
# from util.ADB import ADB
# from util.Constant import *
# from util.License import check_license
# from util.TelegramBot import TelegramBot
# from util.TerraWallet import TerraWallet
# from screen.Connect import Connect
# from screen.ConvertLostCenturia import ConvertLostCenturia
# from screen.Home import Home
# from screen.RecoverWallet import RecoverWallet
#
# logging.basicConfig(
#     level=int(logging.DEBUG),
#     format="%(asctime)s [%(levelname)s] %(threadName)s %(message)s",
#     handlers=[
#         logging.FileHandler("debug.log"),
#         logging.StreamHandler()
#     ]
# )
#
# PACKAGE_NAME = "c2xstation.android"
#
#
# def import_wallet(player, seed_phrase: str):
#     logging.debug("import wallet:" +player.get_title())
#     connect_screen = Connect(player)
#     recover_wallet = RecoverWallet(player)
#     print(connect_screen.is_display())
#     player.clear_app_data(PACKAGE_NAME)
#     player.run_app(PACKAGE_NAME)
#     connect_screen.wait_util_display()
#     time.sleep(2)
#     connect_screen.go_to_recover_wallet()
#
#     recover_wallet.wait_util_display()
#     recover_wallet.import_use_seed_phrase(seed_phrase)
#
#
# def convert_dust_to_lct(player, seed_phrase):
#     home_screen = Home(player)
#     home_screen.goto_convert_lost_centuria()
#
#     convert_lost_centuria_screen = ConvertLostCenturia(player)
#     return convert_lost_centuria_screen.convert_dust_to_lct(seed_phrase)
#
#
# def player_thread(player, seed_phrase):
#     terra_wallet = TerraWallet(seed_phrase)
#     try:
#         # adbplayer.screen_cap()
#         logging.debug("player info: " + player.get_title())
#         logging.debug("seed: " + seed_phrase)
#         import_wallet(player, seed_phrase)
#         result = convert_dust_to_lct(player, seed_phrase)
#         if result:
#             TelegramBot.send_photo_message(player.get_title() + " - " + terra_wallet.get_address(),
#                                            player.get_screenshot_file_path())
#     except Exception as e:
#         logging.exception("Error " + str(e) + " - " + seed_phrase[0:10]+ " - "+player.get_title())
#
#         TelegramBot.send_photo_message(player.get_title() + " - " + terra_wallet.get_address() + " Error:",
#                                        player.get_screenshot_file_path())
#
#
#
# if __name__ == '__main__':
#     if not check_license():
#         sys.exit(0)
#
#     list_seed = []
#     with open(SEED_PATH) as file:
#         list_seed = file.readlines()
#         list_seed = [line.rstrip() for line in list_seed]
#
#     list_device = []
#     list_device_name = LIST_DEVICE.split("|")
#     print(list_device_name)
#
#     for device_name in list_device_name:
#         adbplayer = ADB(device_name)
#         list_device.append(adbplayer)
#     print(len(list_device))
#
#     thread_pool = ThreadPoolExecutor(max_workers=len(list_device))
#
#     index = 0
#     for seed_phrase in list_seed:
#         try:
#             device_index = index % len(list_device)
#             device = list_device[device_index]
#             thread_pool.submit(player_thread, device, seed_phrase)
#         except Exception as e:
#             logging.error("Error " + str(e) + " - " + seed_phrase[0:10])
#
#         index += 1
