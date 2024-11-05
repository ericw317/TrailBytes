from CustomLibs import ShadowCopies
from CustomLibs import time_conversion as TC
import os
import shutil
from Registry import Registry
import codecs

def decode_rot13(string):
    return codecs.decode(string, 'rot13')


# copy locked NTUSER.DAT file
def copy_locked_NTUSER(user):
    try:
        ShadowCopies.create_shadow_copy()  # create shadow copy
        shadow_copy_path = ShadowCopies.get_latest_shadow_copy()  # get latest shadow copy
        NTUSER_source = os.path.join(shadow_copy_path, "Users", str(user), "NTUSER.DAT")  # NTUSER.DAT source path
        destination_path = os.path.join(os.getcwd(), "NTUSER_copy")  # destination to copy NTUSER to

        shutil.copy(NTUSER_source, destination_path)  # copy the NTUSER.DAT file

        # delete shadow copy
        shadow_ID = ShadowCopies.get_latest_shadow_copy_id()  # get shadow copy ID
        ShadowCopies.delete_shadow_copy(shadow_ID)  # delete shadow copy
    except Exception as e:
        print("Error: Make sure you are running as administrator.")

# copy NTUSER.DAT file from mounted drive
def copy_mounted_NTUSER(drive, user):
    NTUSER_path = f"{drive}[root]\\Users\\{user}\\NTUSER.DAT"
    destination_path = os.path.join(os.getcwd(), "NTUSER_copy")
    shutil.copy(NTUSER_path, destination_path)

def find_lnk_guid_path(user_assist_key):
    # Search for the GUID containing LNK files (".yax" in ROT13)
    for GUID in user_assist_key.subkeys():
        for Count in GUID.subkeys():
            for value in Count.values():
                if value.name().endswith(".yax"):
                    clean_path = (user_assist_key.path()).split("Software", 1)[-1]
                    return f"Software{clean_path}\\{GUID.name()}\\Count"
    return None

def decode_data(data):
    if len(data) >= 12:
        last_executed_filetime = int.from_bytes(data[60:68], byteorder="little")
        return last_executed_filetime
    return None


def sanitize_name(name):
    if "{0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}" in name:
        return name.replace("{0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}", "{Common Programs}")
    elif "{9E3995AB-1F9C-4F13-B827-48B24B6C7174}" in name:
        return name.replace("{9E3995AB-1F9C-4F13-B827-48B24B6C7174}", "{User Pinned}")
    elif "{A77F5D77-2E2B-44C3-A6A2-ABA601054A51}" in name:
        return name.replace("{A77F5D77-2E2B-44C3-A6A2-ABA601054A51}", "{Programs}")
    else:
        return name


# parse NTUSER.DAT information
def get_user_assist(drive, user):
    lnk_guid_list = []

    # create NTUSER.DAT copy
    if drive == "C:\\":
        if not os.path.exists("NTUSER_copy"):
            copy_locked_NTUSER(user)
    else:
        if not os.path.exists("NTUSER_copy"):
            copy_mounted_NTUSER(drive, user)

    # open registry file and access user assist key
    reg = Registry.Registry("NTUSER_copy")
    user_assist_key_path = "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist"
    user_assist_key = reg.open(user_assist_key_path)

    # get path with lnk files
    lnk_guid = find_lnk_guid_path(user_assist_key)
    if lnk_guid is None:
        return 0

    # collect contents of LNK GUID folder
    lnk_guid = reg.open(lnk_guid)
    for value in lnk_guid.values():
        if (value.name()).endswith(".yax"):
            # name full path of program
            path = decode_rot13(value.name())

            # sanitize names
            path = sanitize_name(path)

            last_execution = TC.filetime_convert(decode_data(value.value()))  # last execution date

            # add data to list
            if path.endswith(".lnk"):
                path = path[:-4]
            lnk_guid_list.append(["Executed Program", path, last_execution])

    os.remove("NTUSER_copy")
    return lnk_guid_list
