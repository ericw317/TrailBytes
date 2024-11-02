from CustomLibs import time_conversion as TC
import os
from construct import Struct, Int32ul, Int16ul, Int32sl, Bytes

# Define the LNK header structure, which includes file attributes at offset 0x18
LNK_HEADER = Struct(
    "header_size" / Int32ul,
    "clsid" / Bytes(16),
    "flags" / Int32ul,
    "file_attributes" / Int32ul,
    "creation_time" / Int32ul,
    "access_time" / Int32ul,
    "write_time" / Int32ul,
    "file_size" / Int32ul,
    "icon_index" / Int32ul,
    "show_command" / Int32ul,
    "hot_key" / Int16ul,
    "reserved" / Bytes(10)
)

# set path
def set_path(artifact_path, drive):
    if "[root]" in os.listdir(drive):
        path = drive + f"[root]\\{artifact_path}"
    else:
        path = drive + artifact_path

    return path

# get recent logs
def get_recent_logs(drive, user):
    recent_path = set_path(f"Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Recent", drive)
    recent_logs = []  # initialize recent_logs

    # populate recent_logs
    for file in os.listdir(recent_path):
        file_path = os.path.join(recent_path, file)
        m_time = TC.convert_unix_epoch_seconds(os.path.getmtime(file_path))
        # original_path = parse_lnk_path(file_path)
        if os.path.isfile(file_path):
            if is_lnk_directory(file_path):
                recent_logs.append([f"Opened directory:", file, m_time])
            else:
                recent_logs.append([f"Opened file:", file, m_time])

    return recent_logs

# tell if lnk file is a directory or not
def is_lnk_directory(lnk_path):
    with open(lnk_path, 'rb') as file:
        header = LNK_HEADER.parse(file.read(76))  # Header is 76 bytes
        file_attributes = header.file_attributes

        # Check if the directory attribute (0x10) is set
        is_directory = bool(file_attributes & 0x10)

        return is_directory

def parse_lnk_path(lnk_path):
    with open(lnk_path, "rb") as f:
        lnk = LNK_HEADER.parse(f.read(76))  # Read and parse the header
        f.seek(76)  # Move to the Link Target ID List

        # Read and ignore the length of the Link Target ID List (skip 2 bytes)
        f.read(2)

        # Extract the original path (stored as a UTF-16LE encoded string)
        path_bytes = f.read(260)  # Attempt to read the max path size
        original_path = path_bytes.decode("utf-16le", errors="ignore").rstrip("\x00")

        return original_path
