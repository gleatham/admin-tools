#!/bin/bash

check_disk_space="Check Disk Space"
hashy_fim="Hashy FIM"
mount_status="Mount Status"

# Script Names
check_disk_space="Check Disk Space"
hashy_fim="File Integrity Management"
mount_status="Check NFS Mount Status"

# Script Paths
check_disk_space_path="./check_disk_space/main.py"
hashy_FIM_path="./hashy_FIM/hashy_FIM.py"
mount_status_path="./mount_status/mount_status.py"


# Display a menu to choose the script
choice=$(dialog --clear --backtitle "Geoff's Admin Tools" \
        --title "Script Selection" \
        --menu "Select a script to run:" 15 50 4 \
        1 "$check_disk_space" \
        2 "$hashy_fim" \
        3 "$mount_status" \
        2>&1 >/dev/tty)

clear


# Get the script name and path based on the user's choice
case $choice in
    1)
        selected_script="$check_disk_space"
        script_path="$check_disk_space_path"
        ;;
    2)
        selected_script="$hashy_fim"
        script_path="$hashy_FIM_path"
        ;;
    3)
        selected_script="$mount_status"
        script_path="$mount_status_path"
        ;;
    *)
        echo "No valid option selected."
        exit 1
        ;;
esac

# Ask for confirmation
dialog --title "Confirmation" --yesno "Are you sure you want to run $selected_script?"

# Capture the exit status of dialog
response=$?

case $response in
   0)
      echo "Running $selected_script..."
      python3 "$script_path"
      ;;
   1)
      echo "You chose not to run the script."
      var/admin-tools/bash/main.sh
      ;;
   255)
      echo "You pressed ESC."
      exit 1
      ;;
esac

# Clean up the screen
clear