# Python script to make migrating QBittorent to Linux easier by modifying fastresume files  

6/18/2021 - After months of very sporadic times of being able to work on this, version 2 is out.
However, I am keeping version 1 around if for some reason anyone would prefer that.
I am not completely satisfied with version 2 yet.
The main thing is, I would like it to be able to do multiple dry runs with different settings before moving on to actual modification. 

Version 2 is a guided way to back up and rewrite the fastresume files in preparation for importing into Linux.
This is intended to be run on Windows, but it should be able to run on linux as well (the Python script, not the executable). Eventually, this might evolve into a full migration tool.
But for now, it converts from Windows to Linux only. Importing into Linux will have to be manually done.

Also new with this release is an executable download that can be run from a Windows Command Prompt. That way, users unfamiliar with Python don't have to download and install it.
This was done very generically with PyInstaller. This was my first time using it, and I am pleasantly surprised how easy it was.

So, if you use the EXE, you can pretty much ignore the stuff below.
Just download the EXE, run it, and when you have your modified backup of the BT_backup folder, manually import it into Linux.
This program will do the following:  
1. Ask you if you want to do a backup or if you already have one.
2. Either manually or semi-automatically determine replacements of base paths
3. Do a dry run and show you what will change
4. Modify the files in the backup that the program made or that you specified.

If you want to understand how the program semi-automatically determines base paths for replacement, see the wiki page here:  
https://github.com/ctminime/QB_Migrate_to_Linux/wiki/Base-path-replacement-explained

----------------------------------------------------------
----------------------------------------------------------
# Notes for use with the Python scripts

Bencode module can be installed with **"pip install bencode.py"** found here: https://pypi.org/project/bencode.py/

Please do not try and use this without at least a basic understanding of Python.

**BACK UP YOUR FILES BEFORE PROCEEDING!!! THIS WILL OVERWRITE THEM!!!  
CORRUPTION MAY HAPPEN!!! USE AT YOUR OWN RISK!!!**  

I would recommend COPYING the "BT_backup" directory to your desktop and running this script on the backup to ensure the originals are untouched.  
The intent of this is to be able to modify the file locations in the fastresume files to make migrating QBittorrent to Linux easier than manually changing the save path on hundreds of torrents.  
You will need to modify the value for "tor_dir" and "linux_dir_start" to suite your needs.  
In my testing, all of my fastresume files (almost 500) the save_path and qBt-savepath had identical values. I don't know if this is true 100% of the time.  
If for some reason they don't match, this will make them match as it is currently written. I do not know if that will cause a problem  
Example: this will convert the values of "save_path" and "qBt-savepath" from:  
c:\torrent\downloads\faketorrentsite\music  
to:  
/data/torrent/downloads/faketorrentsite/music  
Due to limitations in the bencode.py module, I had to re-write the entire fastresume file instead of just modifying the value in "save_path" and "qBt-savepath"  

**Known Issues:**

1. This will not correct case discrepancies. For example, if the fastresume file points to "c:\torrent\downloads\faketorrentsite\linux_isos" but the actual directory is "c:\torrent\downloads\faketorrentsite\LINUX_ISOS", this works just fine in Windows but will cause a path not found error once converted to nix directory structure. (this is not something I am going to try and fix)
2. (**FIXED**)The script does not currently modify the "mapped_files" section of the fastresume file.  

**This does not include a "how to" to fully migrate QBittorrent to Linux.**
