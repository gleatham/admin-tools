'''
Author: Geoff Leatham
Date: 12/29/2020

This program checks the NFS share status and fixes it as needed.

Variables are hard coded in two places:
-main()
-mount()
'''

import os
from pwd import getpwuid
from os import stat
from datetime import datetime


def log(problem):
    # Log everytime the drive has to be remounted or permissions need changed.
    try:
        fout = open("/home/geoff/Documents/python/mountStatus/log.txt", "a")
        date = datetime.today()
        date = date.strftime('%Y-%m-%d')
        if problem == 1:
            fout.write(date + " Share not mounted\n")
            mount()
        elif problem == 2:
            fout.write(date + " Failed to write to share\n")
            mount()
        elif problem == 3:
            fout.write(date + " Incorrect permissions found\n")
            change_permissions()
        elif problem == 4:
            fout.write(date + " Failed to read from share\n")
            mount()
        fout.close()

        mount()
    except FileNotFoundError:
        return

    return


def mount():
    os.system('umount /fakeNFS')
    os.system('mount /dev/sdb1 /fakeNFS')

    main()


def change_permissions():
    try:
        os.system('chown root:root /fakeNFS')
    except OSError:
        print("Failed to change permissions")

    main()


def check_permissions(c_owner, c_group, path):
    try:
        owner = getpwuid(stat(path).st_uid).pw_name
        group = getpwuid(stat(path).st_gid).pw_name

        if owner != c_owner or group != c_group:
            log(3)
        else:
            return
    except OSError:
        print("Faile to check permissions")


def check_write(write_path):
    # write a small text file and remove it
    try:
        fout = open(write_path, "w")
        fout.write("This is a test")
        fout.close()
    except FileNotFoundError:
        log(2)
        mount()

    return


def check_read(write_path):
    try:
        fin = open(write_path, "r")
        line = fin.readline() # Why did I do this?
        fin.close()
    except FileNotFoundError:
        log(4)


def check_mount(path):
    # returns true if the disk is mounted
    try:
        is_path = os.path.ismount(path)
        if is_path:
            return
        else:
            log(1)
            mount()

    except RuntimeError:
        print("Fatal error: Failed to check mount status")

    return


def main():
    # It will write first then read in order to have a file to read.

    path = "/fakeNFS"
    write_path = "/fakeNFS/testWrite.txt"
    owner = "root"
    group = "root"
    check_mount(path)
    check_write(write_path)
    check_read(write_path)
    check_permissions(owner, group, path)


if __name__ == "__main__":
    main()