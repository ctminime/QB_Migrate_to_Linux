## Python script to make migrating QBittorent to Linux easier by modifying fastresume files  
Originally Written 2/17/2019  

**1/5/2021 - Update coming soon**  

**4/14/2021 - Been a little while (2 months?) since I worked on this.. until last night. The script took on a life of its own. It went from being less than 20 lines of code (excluding comments) to now it is somewhere shy of 200 lines. The new version will be more of a walk-through that has several differnet features including: optional backup, dry runs, and some minor analysis of existing save paths in the fastresume file.**  

**4/25/2021 - Over 200 lines now. Getting close to being done.**  

**5/19/2021 - UHG, tonight was my 1st chance to work on this in almost a month. I have it fully functional now but there are 1 or 2 things I want to improve. If I can't get to it in the next week or so, I will upload it as it is along with an updated readme.**  

This is my first program fresh out of a 1 week course. So, it is probably a little crude.  
Written for Python 3.7.

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

**Issues that I ran into:**

1. This will not correct case discrepancies. For example, if the fastresume file points to "c:\torrent\downloads\faketorrentsite\linux_isos" but the actual directory is "c:\torrent\downloads\faketorrentsite\LINUX_ISOS", this works just fine in Windows but will cause a path not found error once converted to nix directory structure. (this is not something I am going to try and fix)
2. The script does not currently modify the "mapped_files" section of the fastresume file. Again this can lead to a path not found error.  
For example, if 'savepath' = "/torrent/downloads/" and entries in 'mapped_files' = "text_files\{filename} the complete paths in QB may look like this (Notice the change in direction of the slashes):  
/torrent/downloads/text_files\text_file_1.txt  
/torrent/downloads/text_files\text_file_2.txt  
/torrent/downloads/text_files\text_file_3.txt  
/torrent/downloads/text_files\text_file_4.txt  
/torrent/downloads/text_files\text_file_5.txt  
/torrent/downloads/text_files\text_file_6.txt  
/torrent/downloads/text_files\text_file_7.txt  
/torrent/downloads/text_files\text_file_8.txt  
I am going to try an fix this issue. However, in my case, I only had about 10 of these and a couple of the 1st issue, so I just fixed them manually within QB.  

**This does not include a "how to" to fully migrate QBittorrent to Linux.**
