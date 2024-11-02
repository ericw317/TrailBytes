from CustomLibs import SAM_parsing
from CustomLibs import time_conversion as TC
import struct
import os

# set path
def set_path(artifact_path, drive):
    if "[root]" in os.listdir(drive):
        path = drive + f"[root]\\{artifact_path}"
    else:
        path = drive + artifact_path

    return path

# parse $I files
def parse_i_file(file_path):
    with open(file_path, "rb") as f:
        # read and parse binary data
        header = struct.unpack("<Q", f.read(8))[0]
        file_size = struct.unpack("<Q", f.read(8))[0]
        deletion_timestamp = struct.unpack("<Q", f.read(8))[0]
        original_path_bytes = f.read()

        # convert data
        deletion_timestamp = TC.filetime_convert(deletion_timestamp)
        original_path = original_path_bytes.decode("utf-16le").rstrip("\x00")[2:]
        file_name = os.path.basename(original_path)

        metadata = [file_name, original_path, deletion_timestamp]
        return metadata

# get $Recycle.Bin logs
def get_recycle_logs(drive, user):
    RID = SAM_parsing.get_RID(drive, user)
    recycle_path = set_path("$Recycle.Bin", drive)
    recycle_folder = ""
    recycle_logs = []

    # get $Recycle.Bin folder that belongs to user
    for file in os.listdir(recycle_path):
        folder_RID = file.split('-')[-1]
        if int(RID) == int(folder_RID):
            recycle_folder = os.path.join(recycle_path, file)
            break

    # loop through files, parsing information
    for file in os.listdir(recycle_folder):
        file_path = os.path.join(recycle_folder, file)
        if file.startswith("$I"):
            file_metadata = parse_i_file(file_path)
            file_name, original_path, deletion_date = file_metadata
            recycle_logs.append(["Deleted file", original_path, deletion_date])

    return recycle_logs
