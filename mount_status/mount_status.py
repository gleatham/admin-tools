'''
Author: Geoff Leatham
Date: 12/29/2020
Last modified: 12/29/2020

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
            changePermissions()
        elif problem == 4:
            fout.write(date + " Failed to read from share\n")
            mount()
        fout.close()

        mount()
    except:
        return

    return


def mount():
    os.system('umount /fakeNFS')
    os.system('mount /dev/sdb1 /fakeNFS')

    main()


def changePermissions():
    try:
        os.system('chown root:root /fakeNFS')
    except:
        print("Failed to change permissions")

    main()


def checkPermissions(cOwner, cGroup, path):
    try:
        owner = getpwuid(stat(path).st_uid).pw_name
        group = getpwuid(stat(path).st_gid).pw_name

        if owner != cOwner or group != cGroup:
            log(3)
        else:
            return
    except:
        print("Faile to check permissions")


def checkWrite(writePath):
    # write a small text file and remove it
    try:
        fout = open(writePath, "w")
        fout.write("This is a test")
        fout.close()
    except:
        log(2)
        mount()

    return


def checkRead(writePath):
    try:
        fin = open(writePath, "r")
        line = fin.readline()
        fin.close()
    except:
        fin.close()
        log(4)


def checkMount(path):
    # returns true if the disk is mounted
    try:
        isPath = os.path.ismount(path)
        if isPath:
            return
        else:
            log(1)
            mount()

    except:
        print("Fatal error: Failed to check mount status")

    return


def main():
    # It will write first then read in order to have a file to read.

    path = "/fakeNFS"
    writePath = "/fakeNFS/testWrite.txt"
    owner = "root"
    group = "root"
    checkMount(path)
    checkWrite(writePath)
    checkRead(writePath)
    checkPermissions(owner, group, path)


if __name__ == "__main__":
    main()