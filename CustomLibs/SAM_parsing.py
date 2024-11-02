import os
import shutil
import subprocess
from Registry import Registry

# copy the sam file
def copy_sam(drive):
    # make a copy of the registry file
    if drive.upper() != "C:\\":  # copying for mounted drives
        if "[root]" in os.listdir(drive):
            begin_source = drive + f"[root]\\"
        else:
            begin_source = drive

        source = begin_source + f"Windows\\System32\\config\\sam"
        destination = os.path.join(os.getcwd(), f"sam_temp")
        shutil.copy(source, destination)
    else:  # copying for C drive
        command = ["reg", "save", f"hklm\\sam", f"sam_temp"]
        try:
            result = subprocess.run(command, check=True, stdout=subprocess.DEVNULL)
        except PermissionError as e:
            print("Error: Make sure you're running as administrator.")

# get RID of user from SAM file
def get_RID(drive, user):
    # make copy of SAM if it doesn't already exist
    if not os.path.exists("sam_temp"):
        copy_sam(drive)
    reg = Registry.Registry("sam_temp")

    # access key
    key_path = r"SAM\Domains\Account\Users\Names"
    key = reg.open(key_path)

    # navigate to the path of the user and open the user key
    user_path = rf"SAM\Domains\Account\Users\Names\{user}"
    key = reg.open(user_path)
    RID = key.value("").value_type()
    os.remove("sam_temp")
    return RID
