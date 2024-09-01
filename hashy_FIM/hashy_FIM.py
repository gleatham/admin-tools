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
def create_hash(directory, num_directories):
    new_hash = {}
    directory = directory
    num_directories = num_directories
    # TODO: Read the comment below
    #keys = [] I'm not sure why this was originally there but I think it was failing without it.
    keys = list(directory.keys())

    # TODO: Change to for loop
    count = 0
    while count < num_directories:
        temp_dir = directory.get(keys[count])
        sha_hash = hashlib.md5()
        try:
            for root, dirs, files in os.walk(temp_dir):
                for names in files:
                    file_path = os.path.join(root, names)
                    try:
                        fin = open(file_path, 'rb')
                    except FileNotFoundError:
                        print("Unable to open file")
                        continue

                    # TODO: Fix the below jank while loop
                    var = True
                    while var:
                        # Read file in chunks
                        buf = fin.read(4096)
                        if not buf:
                            break
                        sha_hash.update(hashlib.md5(buf).digest())

                    fin.close()

        except NotADirectoryError:
            print("Hashing failed")
            import traceback
            traceback.print_exc(limit=None, file=None, chain=True)
            return -2
        new_hash.update({keys[count]: sha_hash})
        count+=1

    return new_hash


'''
If a new folder is added to the directory list it will create a new hash for it 
and write it to the file.
'''
def write_new_hash(file_path, directories, hashes, num_directories):
    keys = list(hashes.keys())
    need_update = False

    try:
        for count in range(len(keys)):
            if hashes.get(keys[count]) == 'null':
                need_update = True
                new_key = create_hash(directories, num_directories)
                hashes.update({keys[count]: new_key.get(keys[count]).hexdigest()})
            count+=1


    except IndexError:
        import traceback
        traceback.print_exc(limit=None, file=None, chain=True)
        return -2

    try:
        if need_update:
            with open(file_path) as fin:
                directory_text = fin.readlines()
                fin.close()

            fout = open(file_path, 'w')
            fout.write("###BEGIN###:::" + '\n')
            fout.close()
            for line in directory_text:
                if line[0] == '#':
                    if line.strip() == '###BEGIN###:::':
                        continue
                    else:
                        fout = open(file_path, 'a')
                        fout.write(line)
                        fout.close()
                else:
                    #This is where the file updating happens
                    temp_line = line.split(':', 3)
                    key = temp_line[0]
                    path = directories.get(temp_line[0])
                    shisha = hashes.get(temp_line[0])
                    fout = open(file_path, 'a')
                    fout.write(str(key) + ":" + str(path) + ":" + str(shisha) + ":" + '\n')
                    fout.close()


    except FileNotFoundError:
        import traceback
        traceback.print_exc(limit=None, file=None, chain=True)
        return -2

    return 0

'''
Reads in a directory path from a file.
Directory path is used in createHash()
'''
def get_directory(file_path):
    directories = {}

    try:
        with open(file_path) as fin:
            directories_list = fin.readlines()

            for counter in range(len(directories_list)):
                temp_dir_list = directories_list[counter].split(':', 3)
                if temp_dir_list[0][0] != "#":
                    directories.update({temp_dir_list[0]: temp_dir_list[1]})
                counter += 1

    except NotADirectoryError:
        print("getDirectory() failed")
        import traceback
        traceback.print_exc(limit=None, file=None, chain=True)
        return -2

    return directories


'''
Reads file to get keys and hashes
'''
def get_hashes(file_path):
    hashes = {}
    try:
        with open(file_path) as fin:
            hashes_list = fin.readlines()

            for counter in range(len(hashes_list)):
                temp_hash_list = hashes_list[counter].split(':', 3)
                if temp_hash_list[0][0] != "#":
                    hashes.update({temp_hash_list[0]: temp_hash_list[2]})
                counter+=1
    except FileNotFoundError:
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
def compare_hash(hashes, new_hash, num_directories):
    keys = list(hashes.keys())

    compare_results = {}

    for count in range(num_directories):
        hash_one = hashes.get(keys[count])
        hash_two = new_hash.get(keys[count]).hexdigest()

        if hash_one == str(hash_two):
            compare_results.update({keys[count]: True})
        else:
            compare_results.update({keys[count]: False})

        count+=1

    return compare_results
'''
Writes data to log based on whether hashes match or not
'''
def write_log(compare_results, directories):
    date = datetime.today()
    date = date.strftime('%Y-%m-%d')

    file = 'C:\\Users\\Geoff\\Documents\\hashTest\\' + 'log' + date + '.txt'

    fout = open(file, 'w')
    log_header = "Directory hash report for: " + date + '\n'
    fout.write(log_header)
    fout.close()

    try:
        fout = open(file, 'a')


        for name, value in compare_results.items():
            if value:
                value = "PASS"
            else:
                value = "**FAILED HASH**"
            data = (name + "  :" + directories.get(str(name)) + "..." + str(value) + '\n')
            fout.write(data)

    except FileNotFoundError:
        print("write_log() Failed")
        import traceback
        traceback.print_exc(limit=None, file=None, chain=True)
        return -2

    return 0


def main():
    #add function at top to get filepath
    file_path = 'C:\\Users\\Geoff\\Documents\\hashTest\\directories.txt'

    #Dictionaries for directory path and hash
    directories = get_directory(file_path)
    hashes = get_hashes(file_path)

    num_directories = len(directories)
    write_new_hash(file_path, directories, hashes, num_directories)
    new_hash = create_hash(directories, num_directories)

    compare_results = compare_hash(hashes, new_hash, num_directories)
    write_log(compare_results, directories)

if __name__ == "__main__":
    main()