# Version 2.0. Original commit 6/18/2021
# This version is functional
from os import get_terminal_size
from shutil import copytree
from sys import platform
from os import listdir
from os import getenv
from os import path
from re import sub
from bencode import bwrite, bread


def yes_or_no(question):
    answer1 = ""
    while answer1 not in ("yes", "no", "quit"):
        answer = input(question)
        answer1 = answer.lower()
        if answer1 == "yes":
            return answer1
        elif answer1 == "no":
            return answer1
        elif answer1 == "quit":
            exit()
        else:
            print("invalid input")


def fr_read(tor_dir, file):
    file_path_name = path.join(tor_dir, file)
    # Set variable for the contents of each fastresume file
    torrent = bread(file_path_name)
    # Set the variable for the original "save_path" value
    fr_read.save_path_orig = (torrent['save_path'])


def get_int_in_range(prompt):
    while True:
        try:
            integer_value = int(input(prompt))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        # if you need to go more than 5 directory levels deep, change here.
        if integer_value < 1 or integer_value > 5:
            print("Value is out of acceptable range. Try again.")
            continue
        else:
            return integer_value


def bencode_ops(tor_dir, base_paths_to_be_replaced1, substituted_base_paths1, dry_run):
    bencode_ops.unmodified = []
    displayed_lines = 0
    for file in listdir(tor_dir):
        if file.endswith(".fastresume"):
            modified = False
            # Set variable for each file name
            file_path_name = path.join(tor_dir, file)
            # Set variable for the contents of each fastresume file
            torrent = bread(file_path_name)
            # Set the variable for the original "save_path" value
            save_path_orig = (torrent['save_path'])
            for s, d in zip(base_paths_to_be_replaced1, substituted_base_paths1):
                if modified is False:
                    if s in save_path_orig:
                        modified = True
                        # Replace the specified portion of the original path "s" with the desired replacement "d".
                        save_path1 = save_path_orig.replace(s, d)
                        # Replace rest of the backslashes with forward slashes
                        save_path2 = sub("\\\\", "/", save_path1)
                        # Replace value of dictionary item "save_path" with the linux equivalent
                        if dry_run is False:
                            torrent['save_path'] = save_path2
                        # Replace value of dictionary item "qBt-savePath" with the linux equivalent
                        if dry_run is False:
                            torrent['qBt-savePath'] = save_path2
                        # Print the new torrent path
                        print(save_path_orig+" ----converts to---- "+save_path2)
                        displayed_lines = displayed_lines + 1
                        if displayed_lines >= line_height:
                            input("Press Enter to Continue...")
                            displayed_lines = 0
                        if 'mapped_files' in torrent:
                            mf_orig1 = (torrent['mapped_files'])
                            mf_orig2 = str(mf_orig1)
                            mf_fixed = sub("\\\\\\\\", "/", mf_orig2)
                            if dry_run is False:
                                torrent['mapped_files'] = mf_fixed
                            print(file+" contains \'mapped_files\'")
                            displayed_lines = displayed_lines + 1
                            if displayed_lines >= line_height:
                                input("Press Enter to Continue...")
                                displayed_lines = 0
                            print(mf_orig2+"\r\n----converts to----\r\n"+mf_fixed)
                            displayed_lines = displayed_lines + 3
                            if displayed_lines >= line_height:
                                input("Press Enter to Continue...")
                                displayed_lines = 0
                        # Write the modified dictionary back to the fastresume file
                        if dry_run is False:
                            bwrite(torrent, file_path_name)
            if modified is False:
                bencode_ops.unmodified.append("NO CHANGE:"+file+" did not match any specified path. " + save_path_orig)


try:
    size = get_terminal_size()
    line_height = size[1] - 1
except OSError:
    line_height = 29
    # print(line_height)

print("Welcome to QB_migrate_to_Linux_v2.\r\n\
This program will help guide you through converting your fastresume files so that they can be imported"
      " into qBittorrent on Linux.\r\n")
# This section determines if the OS is Windows or Linux to set the appropriate default BT_backup folder location.
if platform == "win32":
    # Get the current user profile in Windows
    upd = (getenv('USERPROFILE'))
    # Windows default BT Backup location excluding user profile
    qbd = "\\AppData\\Local\\qBittorrent\\BT_backup"
    # Combined to get full path
    dqbtb = upd + qbd
    bt = "\\BT_backup\\"
# The Linux check here still needs validation.
elif "linux" in platform:
    # Get the current user profile in Linux
    upd = (getenv('HOME'))
    # Linux default BT Backup location excluding user profile
    qbd = "/.local/share/data/qBittorrent/BT_backup"
    # Combined to get full path
    dqbtb = upd + qbd
    bt = "/BT_backup/"
else:
    print(
        "OS does not appear to be Windows or Linux. Setting default qBittorrent default BT_backup folder"
        " location to NULL")
    dqbtb = "NULL"
    bt = ""

# This section checks to see if you already have a backup and makes a backup if you don't have one.
q3 = yes_or_no(
    "Do you already have a backup of the BT_backup folder where the fastresume files are stored?\r\n--"
    "Enter either yes/no to continue or quit to exit: ")
bak_loc = ""
if q3 == "no":
    print("Since you do not have a backup, it is time to make a one.")
    q5 = yes_or_no(
        "Is this the location of your BT_backup folder? "
        + dqbtb + "\r\n--Enter either yes/no to continue or quit to exit: ")
    if q5 == "yes":
        pass
    elif q5 == "no":
        q7 = input("Where is your BT_backup file located?: ")
        while path.exists(q7) is False:
            q7 = input("Path does not exist. Please enter a valid path: ")
        dqbtb = q7
        print(dqbtb)
    else:
        print("error q5")
        exit()
    q6 = input("Where would you like the backup to be made?: ")
    while path.exists(q6) is False:
        q6 = input("Path does not exist. Please enter a valid path: ")
    bak_loc = q6 + bt
    dir_check = path.exists(bak_loc)
    while dir_check is True:
        q9 = input(
            "BT_backup Folder already exists here. Please input a different location.\r\nWhere"
            " would you like the backup to be made?: ")
        bak_loc = q9
        dir_check = path.exists(bak_loc)
    print("Copying folder")
    copytree(dqbtb, bak_loc)
elif q3 == "yes":
    print("You said you already have a backup")
    q8 = input("Where is your backup of the BT_backup folder located?: ")
    while path.exists(q8) is False:
        q8 = input("Path does not exist. Please enter a valid path: ")
    bak_loc = q8
else:
    print("error q3")
    exit()

# print(dir_check)
base_paths_to_be_replaced = []
substituted_base_paths = []
q2 = yes_or_no("This program can help determine which base paths should be replaced.\r\n"
               "If you want to do this, enter 'yes'.\r\n"
               "If not, and you would prefer to do it all manually, enter 'no'\r\n"
               "Or 'quit' to exit the program: "
               )
if q2 == "no":
    while True:
        q4 = yes_or_no("Do you have another directory pair? \r\n--Enter either yes/no to continue or quit to exit: ")
        if q4 == "yes":
            tor_start = input("Enter the part of the path you want to replace: ")
            tor_replace = input("What do you want to replace " + tor_start + " with: ")
            base_paths_to_be_replaced.append(tor_start)
            substituted_base_paths.append(tor_replace)
            continue
        elif q4 == "no":
            break
        else:
            print("error q4")
            exit()
elif q2 == "yes":
    spo_list = []
    for file1 in listdir(bak_loc):
        if file1.endswith(".fastresume"):
            # Set variable for each file name
            fr_read(bak_loc, file1)
            spo_list.append(fr_read.save_path_orig)
    # print(spo_list)
    print("This part of the program will try to automatically determine the base directories that need to be converted.\r\n"
          "But before we do that, we need to determine how many directory levels deep you want to convert separately.\r\n"
          "The deeper the level you go, the more you will need to specify what directory replaces those.\r\n"
          "For instance 1 directory level deep is just the drive letter like 'c:\\'.\r\n"
          "Or 4 directory levels might be something like 'C:\\Users\\user\\Downloads\\'.\r\n"
          "I would recommend starting with 1 and go deeper if necessary.\r\n"
          )
    dir_deep = get_int_in_range("Please enter the number directories deep: ")
    # print(dir_deep)
    sorting = {}
    for p in spo_list:
        # This returned empty splits (just leaving this here for explanation).
        # x = p.split('\\')
        # This filters out empty splits so that a path can be reconstructed properly
        f = filter(None, p.split('\\'))
        x = list(f)
        # This section counts to the specified directory depth and adds only unique values to "base_paths_to_be_replaced" list.
        path_depth = x[:dir_deep]
        asdfg = ""
        sub_count = 0
        for i in path_depth:
            asdfg = asdfg + str(i) + "\\"
            sub_count = sub_count + 1
        sorting[asdfg] = sub_count
        # print(asdfg)
        # print(sub_count)
    # print(sorting)
    # Sort longest to shortest so that a standalone drive letter is last (example z:\). This is an attempt to get most specific to least specific.
    sorted_paths_dict = dict(sorted(sorting.items(), key=lambda item: item[1], reverse=True))
    print("These are the base directories that you need to replace with a Linux equivalent.")
    check_replacement_list = []
    for spd in sorted_paths_dict:
        print(spd)
    for v in sorted_paths_dict:
        base_paths_to_be_replaced.append(v)
    for x in base_paths_to_be_replaced:
        # print(x)
        tor_replace = input("What do you want to replace \"" + x + "\" with?: ")
        # This checks the 1st character in the replacement base path to ensure it starts with "/"
        while tor_replace[0] != '/':
            tor_replace = input("Uh, That doesn't look like a Linux path. What do you want to replace \"" + x + "\" with?: ")
        # Add tailing "/" if it isn't there.
        if tor_replace[-1] == "/":
            substituted_base_paths.append(tor_replace)
        else:
            tor_replace = tor_replace + "/"
            substituted_base_paths.append(tor_replace)
        hhhhh = tor_replace + " replaces " + x
        check_replacement_list.append(hhhhh)
    for rpl in check_replacement_list:
        print(rpl)
    # print(substituted_base_paths)
else:
    print("error q2")
    exit()

input("Time to do a dry run. Press Enter to Continue...")
# print(base_paths_to_be_replaced, substituted_base_paths)
bencode_ops(bak_loc, base_paths_to_be_replaced, substituted_base_paths, dry_run=True)
# print(bencode_ops.unmodified)
unmodified_count = len(bencode_ops.unmodified)
# print(unmodified_count)
# The original wording of this was "if not unmodified" before making the def bencode_ops. That wording made me chuckle when I first wrote it.
# This is just checking to see if the list "unmodifed" is empty. If it is not empty, list the files and the path.
if not bencode_ops.unmodified:
    pass
else:
    print("#############################################################################################")
    for u in bencode_ops.unmodified:
        print(u)
    print("#############################################################################################")

q1 = yes_or_no("Would like to proceed with modifying the files? \r\n--Entering No or Quit will exit the program: ")
if q1 == "no":
    print("Exiting...")
    exit()
elif q1 == "yes":
    print("modifying files")
    bencode_ops(bak_loc, base_paths_to_be_replaced, substituted_base_paths, dry_run=False)
else:
    print("error q1")
    exit()