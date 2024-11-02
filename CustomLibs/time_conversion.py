import datetime
from zoneinfo import ZoneInfo
import config

# convert FILETIME format to readable
def filetime_convert(filetime):
    seconds = filetime / 10**7  # convert FILETIME to seconds
    filetime_epoch = datetime.datetime(1601, 1, 1, tzinfo=datetime.timezone.utc)  # define epoch
    readable_time = filetime_epoch + datetime.timedelta(seconds=seconds)  # add seconds to epoch
    readable_time = readable_time.replace(microsecond=0)

    if config.timezone != "UTC":
        local_time = readable_time.astimezone(ZoneInfo(config.timezone))
        return local_time
    else:
        return readable_time

# convert windows epoch to readable
def convert_windows_epoch(timestamp):
    epoch_start = datetime.datetime(1601, 1, 1, tzinfo=datetime.timezone.utc)
    timestamp_in_seconds = timestamp / 1_000_000
    readable_time = epoch_start + datetime.timedelta(seconds=timestamp_in_seconds)
    readable_time = readable_time.replace(microsecond=0)  # remove microseconds

    if config.timezone != "UTC":
        local_time = readable_time.astimezone(ZoneInfo(config.timezone))
        return local_time
    else:
        return readable_time

# convert unix epoch in microseconds
def convert_unix_epoch_microseconds(timestamp):
    epoch_start = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    readable_time = epoch_start + datetime.timedelta(microseconds=timestamp)
    readable_time = readable_time.replace(microsecond=0)

    if config.timezone != "UTC":
        local_time = readable_time.astimezone(ZoneInfo(config.timezone))
        return local_time
    else:
        return readable_time

# convert unix epoch in seconds
def convert_unix_epoch_seconds(timestamp):
    epoch_start = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    readable_time = epoch_start + datetime.timedelta(seconds=timestamp)
    readable_time = readable_time.replace(microsecond=0)

    if config.timezone != "UTC":
        local_time = readable_time.astimezone(ZoneInfo(config.timezone))
        return local_time
    else:
        return readable_time
