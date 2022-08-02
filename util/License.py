import re
import subprocess

from util.Constant import *

list_key = [
    'TEST1-9959A1A8-F912-0000-0000-000000000000',
    'KY-A0DF41F8-1809-4B3A-92A2-56AC58FC027A',
    'THAI-2D355419-F561-FF5C-83CE-FC3497125EA0'
    'KY-PC-A1CD3942-2F8A-DA1E-ACD9-D8BBC16DA346',
    'THAI-2D355419-F561-FF5C-83CE-FC3497125EA0',
    'HOA-9959A1A8-F217-0000-0000-00000000000'
    'KY-03000200-0400-0500-0006-000700080009'
]


def getUUID():
    s = subprocess.check_output('wmic csproduct get UUID').decode('UTF-8').replace("UUID", "")
    s = re.sub(r"\s+", "", s)
    return s


def check_license():
    return COMPUTER_NAME + "-" + getUUID() in str(list_key)
    return True


if __name__ == '__main__':
    print(getUUID())
    print(check_license())
