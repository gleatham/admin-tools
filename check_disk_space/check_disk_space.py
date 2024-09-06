import os


class CheckDiskspace:
    def __init__(self):
        self.tool_name = "CheckDiskspace"

    def get_name(self):
        print(f"Tool: {self.tool_name}")

    def check_disk_space(self):
        current_host = ""
        with open("df-output.txt", "r") as file:
            for line in file:
                line = line.split()
                if len(line) < 6:
                    if len(line) > 3:
                        current_host = line[0]
                        print(f"Failed to get details from {current_host}.")
                        # TODO: write failed hostname to email file
                else:
                    if str(line[0]) == "Filesystem":
                        continue
                    elif str(line[2]) == "CHANGED":
                        current_host = str(line[0])
                    elif str(line[5][0]) == "/":
                        # TODO: write hostname and path to email file if usage
                        #  is >90%
                        usage_percentage = str(line[4])
                        usage_percentage = usage_percentage[:-1]
                        if int(usage_percentage) > 89:
                            print(f"Usage on {current_host} {line[5]} at {usage_percentage}%")
                    else:
                        print("No matching pattern was found.")

    def create_df(self):
        # ansible will generate this
        df = "df -h"
        os.system(df)

    def create_file(self):
        # TODO: create file name based on date and time for the email attachement
        pass

    def send_email(self):
        # TODO: send email only if data has been written to the file
        pass

    def run(self):
        self.check_disk_space()
        # parse and check file
        # email alert if disks are full
