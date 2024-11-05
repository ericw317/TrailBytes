from CustomLibs import InputValidation as IV
from CustomLibs import list_functions as LF
from CustomLibs import recent_parsing
from CustomLibs import recycle_bin_parsing
from CustomLibs import NTUSER_parsing
import config
import psutil
import os

# set timezone
def get_timezone():
    # prompt time zone selection
    timezone_list = ["America/New_York (EST/EDT)", "America/Chicago (CST/CDT)", "America/Denver (MST/MDT)",
                     "America/Los_Angeles (PST/PDT)", "Europe/London (GMT/BST)", "Europe/Paris (CET/CEST)",
                     "Asia/Tokyo (JST)", "Asia/Shanghai (CST)", "Australia/Sydney (AEST/AEDT)", "UTC"]

    timezone_select = IV.int_between_numbers(
        f"Select a timezone to display timestamps in: {LF.print_list_numbered(timezone_list)}\n",
        1, len(timezone_list))

    config.timezone = timezone_list[timezone_select - 1].split(" ")[0]

# list drives
def list_drives():
    counter = 1
    partitions = psutil.disk_partitions()
    drives = {}

    # add each drive to a dictionary and enumerate each entry
    for partition in partitions:
        drives[counter] = partition.device
        counter += 1

    return drives

# get drive
def get_drive(drives):
    # prompt for drive selection
    print("Enter the number of the device you want to analyze: ")
    for number, drive in drives.items():  # print all connected devices
        print(f"{number}: {drive}")
    print("0: Exit Program")
    drive_selected = IV.int_between_numbers("", 0, len(drives))  # get input on which drive to analyze
    if drive_selected == 0:
        return 0
    return drives[drive_selected]  # map input to drive

# set path
def set_path(artifact_path, drive):
    if "[root]" in os.listdir(drive):
        path = drive + f"[root]\\{artifact_path}"
    else:
        path = drive + artifact_path

    return path

# get users
def get_users(drive):
    user_exclusion = ["Default", "Default User", "Public", "All Users"]  # exclusion list
    users_path = set_path("Users", drive)  # set path to users folder
    user_list = []

    # populate user list
    for user in os.listdir(users_path):
        if os.path.isdir(os.path.join(users_path, user)) and user not in user_exclusion:
            user_list.append(user)

    # prompt user selection
    user_selection = IV.int_between_numbers(f"Select a user: {LF.print_list_numbered(user_list)}\n",
                                            1, len(user_list))

    return user_list[user_selection - 1]

# combine logs
def combine_logs(main_log, append_log):
    for element in append_log:
        main_log.append(element)

    return main_log


artifact_menu = True

def main():
    all_logs = []
    get_timezone()
    drive_list = list_drives()
    drive = get_drive(drive_list)
    user = get_users(drive)

    # gather logs
    try:
        recent_logs = recent_parsing.get_recent_logs(drive, user)
    except Exception:
        recent_logs = []
    try:
        recycle_logs = recycle_bin_parsing.get_recycle_logs(drive, user)
    except Exception:
        recycle_logs = []
    try:
        user_assist_logs = NTUSER_parsing.get_user_assist(drive, user)
    except Exception:
        user_assist_logs = []

    # combine logs and sort
    all_logs = combine_logs(all_logs, recent_logs)
    all_logs = combine_logs(all_logs, recycle_logs)
    all_logs = combine_logs(all_logs, user_assist_logs)
    all_logs = sorted(all_logs, key=lambda x: x[2])

    # get spacing
    activity_spacing = 30
    spacing = 0
    for log in all_logs:
        if len(log[1]) > spacing:
            spacing = len(log[1])
    spacing += 10

    # output logs to a file
    with open(f"{user} Activity Log.txt", 'w') as file:
        file.write(f"{'Activity':<{activity_spacing}}{'File':<{spacing}}Timestamp\n")
        file.write("-" * (activity_spacing + spacing + 25) + "\n")
        for log in all_logs:
            file.write(f"{log[0]:<{activity_spacing}}{log[1]:<{spacing}}{log[2]}\n")

    # print logs
    print(f"{'Activity':<{activity_spacing}}{'File':<{spacing}}Timestamp")
    print("-" * (activity_spacing + spacing + 25))
    for log in all_logs:
        print(f"{log[0]:<{activity_spacing}}{log[1]:<{spacing}}{log[2]}")

    print(f"\nLogs saved to '{user} Activity Log.txt'")


if __name__ == "__main__":
    main()
