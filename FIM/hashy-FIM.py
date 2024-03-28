import os
import hashlib
from datetime import datetime

'''
Receives a dictionary of directories.
Iterates through the dictionary creating a hash for each value and writes it to a new dictionary
with a matching key.
directory - dictionary
numDirectories - int 
'''
def createHash(directory, numDirectories):
    newHash = {}
    directory = directory
    numDirectories = numDirectories
    keys = []
    keys = list(directory.keys())

    count = 0
    while(count < numDirectories):
        tempDir = directory.get(keys[count])
        SHAhash = hashlib.md5()
        try:
            for root, dirs, files in os.walk(tempDir):
                for names in files:
                    filepath = os.path.join(root, names)
                    try:
                        fin = open(filepath, 'rb')
                    except:
                        print("Unable to open file")
                        fin.close()
                        continue

                    var = True
                    while var:
                        # Read file in chunks
                        buf = fin.read(4096)
                        if not buf:
                            break
                        SHAhash.update(hashlib.md5(buf).digest())

                    fin.close()

        except:
            print("Hashing failed")
            import traceback
            traceback.print_exc(limit=None, file=None, chain=True)
            return -2
        newHash.update({keys[count]: SHAhash})
        count+=1

    return newHash


'''
If a new folder is added to the directory list it will create a new hash for it 
and write it to the file.
'''
def writeNewHash(filePath, directories, hashes, numDirectories):
    keys = list(hashes.keys())
    needUpdate = False

    try:
        for count in range(len(keys)):
            if(hashes.get(keys[count]) == 'null'):
                needUpdate = True
                newKey = createHash(directories, numDirectories)
                hashes.update({keys[count]: newKey.get(keys[count]).hexdigest()})
            count+=1


    except:
        import traceback
        traceback.print_exc(limit=None, file=None, chain=True)
        return -2

    try:
        if(needUpdate == True):
            with open(filePath) as fin:
                directoryText = fin.readlines()
                fin.close()

            fout = open(filePath, 'w')
            fout.write("###BEGIN###:::" + '\n')
            fout.close()
            for line in directoryText:
                if(line[0] == '#'):
                    if(line.strip() == '###BEGIN###:::'):
                        continue
                    else:
                        fout = open(filePath, 'a')
                        fout.write(line)
                        fout.close()
                else:
                    #This is where the file updating happens
                    tempLine = line.split(':', 3)
                    key = tempLine[0]
                    path = directories.get(tempLine[0])
                    shisha = hashes.get(tempLine[0])
                    fout = open(filePath, 'a')
                    fout.write(str(key) + ":" + str(path) + ":" + str(shisha) + ":" + '\n')
                    fout.close()


    except:
        import traceback
        traceback.print_exc(limit=None, file=None, chain=True)
        return -2

    return 0

'''
Reads in a directory path from a file.
Directory path is used in createHash()
'''
def getDirectory(filePath):
    directories = {}

    try:
        with open(filePath) as fin:
            directoriesList = fin.readlines()

            for counter in range(len(directoriesList)):
                tempDirList = directoriesList[counter].split(':', 3)
                if (tempDirList[0][0] != "#"):
                    directories.update({tempDirList[0]: tempDirList[1]})
                counter += 1

    except:
        print("getDirectory() failed")
        import traceback
        traceback.print_exc(limit=None, file=None, chain=True)
        return -2

    return directories


'''
Reads file to get keys and hashes
'''
def getHashes(filePath):
    hashes = {}
    try:
        with open(filePath) as fin:
            hashesList = fin.readlines()

            for counter in range(len(hashesList)):
                tempHashList = hashesList[counter].split(':', 3)
                if(tempHashList[0][0] != "#"):
                    hashes.update({tempHashList[0]: tempHashList[2]})
                counter+=1
    except:
        print("getHashes() Failed")
        import traceback
        traceback.print_exc(limit=None, file=None, chain=True)
        return -2
    return hashes


'''
Receives two dictionaries and compares hashes based on matching keys
Returns dictionary with the same key as all the other dicts
If the hashes match the value is True else False
'''
def compareHash(hashes, newHash, numDirectories):
    keys = list(hashes.keys())

    compareResults = {}

    for count in range(numDirectories):
        hashOne = hashes.get(keys[count])
        hashTwo = newHash.get(keys[count]).hexdigest()

        if(hashOne == str(hashTwo)):
            compareResults.update({keys[count]: True})
        else:
            compareResults.update({keys[count]: False})

        count+=1

    return compareResults
'''
Writes data to log based on whether hashes match or not
'''
def writeLog(compareResults, directories):
    date = datetime.today()
    date = date.strftime('%Y-%m-%d')

    file = 'C:\\Users\\Geoff\\Documents\\hashTest\\' + 'log' + date + '.txt'

    fout = open(file, 'w')
    logHeader = "Directory hash report for: " + date + '\n'
    fout.write(logHeader)
    fout.close()

    try:
        fout = open(file, 'a')


        for name, value in compareResults.items():
            if(value == True):
                value = "PASS"
            else:
                value = "**FAILED HASH**"
            data = (name + "  :" + directories.get(str(name)) + "..." + str(value) + '\n')
            fout.write(data)

    except:
        print("writeLog() Failed")
        import traceback
        traceback.print_exc(limit=None, file=None, chain=True)
        return -2

    return 0


def main():
    #add function at top to get filepath
    filePath = 'C:\\Users\\Geoff\\Documents\\hashTest\\directories.txt'

    #Dictionaries for directory path and hash
    directories = getDirectory(filePath)
    hashes = getHashes(filePath)

    numDirectories = len(directories)
    writeNewHash(filePath, directories, hashes, numDirectories)
    newHash = createHash(directories, numDirectories)

    compareResults = compareHash(hashes, newHash, numDirectories)
    writeLog(compareResults, directories)

if __name__ == "__main__":
    main()