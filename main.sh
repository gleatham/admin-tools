#!/bin/bash

check_disk_space = "Check Disk Space"
hasy_FIM = "Hashy FIM"
mount_status = "Mount Status"

check_disk_space_path = "./check_disk_space/main.py"
hashy_FIM_path = "./hashy_FIM/hashy_FIM.py"
mount_status = "./mount_status/mount_status.py"

# Display a menu to choose the script
choice=$(dialog --clear --backtitle "Geoff's Admin Tools" \
        --title "Script Selection" \
        --menu "Select a script to run:" 15 50 4 \
        1 "$script1" \
        2 "$script2" \
        3 "$script3" \
        2>&1 >/dev/tty)

clear

# Get the script name and path based on the user's choice
case $choice in
    1)
        selected_script="$script1"
        script_path="$path1"
        ;;
    2)
        selected_script="$script2"
        script_path="$path2"
        ;;
    3)
        selected_script="$script3"
        script_path="$path3"
        ;;
    *)
        echo "No valid option selected."
        exit 1
        ;;
esac

# Ask for confirmation
dialog --title "Confirmation" --yesno "Are you sure you want to run $selected_script?" 7 60

# Capture the exit status of dialog
response=$?

case $response in
   0)
      echo "Running $selected_script..."
      python3 "$script_path"
      ;;
   1)
      echo "You chose not to run the script."
      ;;
   255)
      echo "You pressed ESC."
      ;;
esac

# Clean up the screen
clear