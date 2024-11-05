import subprocess
import re

# create shadow copy
def create_shadow_copy():
    # Create a shadow copy
    result = subprocess.run("wmic shadowcopy call create Volume='C:\\'", shell=True, capture_output=True, text=True)

# get latest shadow copy
def get_latest_shadow_copy():
    # run "vssadmin list shadows" command to list all shadow copies
    result = subprocess.run(['vssadmin', 'list', 'shadows'], stdout=subprocess.PIPE, text=True)

    # find all 'Shadow Copy Volume' paths
    shadow_copy_paths = re.findall(r'Shadow Copy Volume: (\\\\\?\\GLOBALROOT\\Device\\HarddiskVolumeShadowCopy\d+)',
                                   result.stdout)

    if shadow_copy_paths:
        latest_shadow_copy = shadow_copy_paths[-1]
        return latest_shadow_copy
    else:
        return None

# get latest_shadow_copy_id
def get_latest_shadow_copy_id():
    # Run "vssadmin list shadows" to list all shadow copies
    result = subprocess.run(['vssadmin', 'list', 'shadows'], stdout=subprocess.PIPE, text=True)

    # Find all 'Shadow Copy ID' entries
    shadow_copy_ids = re.findall(r'Shadow Copy ID: ({[a-f0-9\-]+})', result.stdout)

    if shadow_copy_ids:
        latest_shadow_copy_id = shadow_copy_ids[-1]  # Get the last (most recent) Shadow Copy ID
        return latest_shadow_copy_id
    else:
        raise Exception("No shadow copies found.")

# delete shadow copy
def delete_shadow_copy(shadow_copy_ID):
    # Run vssadmin delete shadows with the specific shadow copy path
    result = subprocess.run(
        ['vssadmin', 'delete', 'shadows', '/Shadow=' + shadow_copy_ID, "/Quiet"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
