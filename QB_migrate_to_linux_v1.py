# 1.0 Originally written on 2/17/2019
# This is my first program fresh out of a 1 week course. So, it is probably a little crude.
# This was written for Python 3.7.
# Bencode module can be installed with "pip install bencode.py" found here: https://pypi.org/project/bencode.py/
# Please do not try and use this without at least a basic understanding of Python.
# AND read through the script to ensure you understand what it is doing. 
# BACK UP YOUR FILES BEFORE PROCEEDING!!! THIS WILL OVERWRITE THEM!!!
# CORRUPTION MAY HAPPEN!!! USE AT YOUR OWN RISK!!!
# I would recommend COPYING the "BT_backup" directory to your desktop and running this script on the backup to ensure the originals are untouched.
# The intent of this is to be able to modify the file locations in the fastresume files to make migrating QBittorrent to Linux easier than manually changing the save path on hundreds of torrents.
# You will need to modify the value for "tor_dir" and "linux_dir_start" to suit your needs.
# In my testing, all of my fastresume files (almost 500) the save_path and qBt-savepath had identical values. I don't know if this is true 100% of the time.
# If for some reason they don't match, this will make them match as it is currently written. I do not know if that will cause a problem
# Example: this will convert the values of "save_path" and "qBt-savepath" from c:\torrent\downloads\faketorrentsite\music to /data/torrent/downloads/faketorrentsite/music
# Due to limitations in the bencode.py module, I had to re-write the entire fastresume file instead of just modifying the value in "save_path" and "qBt-savepath"
# Release notes:
# Version 1.1: Made small modifications to be formatted according to PEP 8. Added "mapped_files" section. Made it easy to do a dry run.
import os
import bencode
from re import sub

# MODIFY these 2 values to suit your needs
# Directory where your QBittorrent fastresume files are
tor_dir = "C:\\Users\\user\\Desktop\\BT_backup\\"
# Start of linux file structure for torrents
linux_dir_start = "/data/"

# For each file in the directory that has the extension ".fastresume"
for file in os.listdir(tor_dir):
    if file.endswith(".fastresume"):
        # Set variable for each file name
        file_path_name = os.path.join(tor_dir, file)
        # Set variable for the contents of each fastresume file
        torrent = bencode.bread(file_path_name)
        # Set the variable for the original "save_path" value
        save_path_orig = (torrent['save_path'])
        # Replace {x}:\ with linux_dir_start (ie "c:\" converts to "/data/").
        # RegEx notes -- Triple escape backslash. Period = any drive letter. Carrot "^" indicates beginning of string.
        save_path1 = sub("^.:\\\\", linux_dir_start, save_path_orig)
        # Replace rest of the backslashes with forward slashes.
        save_path2 = sub("\\\\", "/", save_path1)
        # Replace value of dictionary item "save_path" with the linux equivalent.
        torrent['save_path'] = save_path2
        # Replace value of dictionary item "qBt-savePath" with the linux equivalent.
        torrent['qBt-savePath'] = save_path2
        # Print the new torrent path
        print(save_path_orig+" ----converts to---- "+save_path2)
        # This section check if the fastresume file has a section called "mapped_files" and replaces the backslashes with forward slashes.
        if 'mapped_files' in torrent:
            mf_orig1 = (torrent['mapped_files'])
            mf_orig2 = str(mf_orig1)
            mf_fixed = sub("\\\\\\\\", "/", mf_orig2)
            torrent['mapped_files'] = mf_fixed
            print(file+" contains \'mapped_files\'")
            print(mf_orig2+"\r\n----converts to----\r\n"+mf_fixed)
        # Write the modified dictionary back to the fastresume file. Comment the following line out for a dry run.
        bencode.bwrite(torrent, file_path_name)

