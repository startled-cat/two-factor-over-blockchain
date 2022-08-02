import os
import time
from termcolor import colored, cprint


data_directory = f"/home/adamko-wsl/git/two-factor-over-blockchain/data/benchmark/network"
file_regex = ".json"

# recursively list files from a directory
def list_files(directory, file_regex):
    files = []
    for f in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, f)):
            if file_regex in f:
                files.append(os.path.join(directory, f))
        else:
            files.extend(list_files(os.path.join(directory, f), file_regex))
    return files

def main():
    files = list_files(data_directory, file_regex)
    # sort files by modofied date
    # files.sort(key=lambda x: -os.path.getmtime(x))
    files.sort()
    healthly_counter = 0
    time_between_tests=60
    for f in files:
        tests_started = 0
        #replace filename in file path with "pid.txt"
        pid_file_path = "/".join(f.split("/")[:-1]) + "/pid.txt"
        with open(pid_file_path, "r") as file:
            tests_started = len(file.readlines())

        tests_finished = 0
        log_file_path = f.replace(".json", ".log")
        with open(log_file_path, "r") as log_file:
            # fidn occurenced of "writing stats" in log file
            tests_finished = 0
            for line in log_file:
                if "writing stats" in line:
                    tests_finished += 1
        
        file_size = os.path.getsize(f)
        # convert size to kilobytes
        file_size = file_size / 1024
        
        modified_time = os.path.getmtime(f)
        
        # get time since file was last modified
        time_since_modified = time.time() - os.path.getmtime(f)
        # format time duration
        time_since_modified_f = time.strftime("%H:%M:%S", time.gmtime(time_since_modified))
        modified_time_f = time.strftime("%D %H:%M:%S", time.gmtime(modified_time))
        
        network = f.split("/")[-2]
        f = f.split("/")[-1]
        network = network + " "*(16-len(network))
        f = f + " "*(38-len(f))
        
        tests_percent = (tests_finished / tests_started) * 100 
        test_percent_emoji = "💚" if tests_percent > 90 else "💛" if tests_percent > 50 else "💜"
        
        msg = f"{network}-> ({tests_started:3d}/{tests_finished:3d}, {tests_percent:3.0f}% {test_percent_emoji})\t{modified_time_f} ({time_since_modified_f} ago) "
        # color text green if time since modofied is less than 15minutes
        if time_since_modified < time_between_tests*60:
            healthly_counter += 1
            cprint(msg, "green")
        elif time_since_modified < (time_between_tests+5)*60:
            cprint(msg, "yellow", on_color="on_yellow", attrs=["bold"])
        elif time_since_modified < (time_between_tests+10)*60:
            cprint(msg, "red", on_color="on_red", attrs=["bold"])
        else:
            cprint(msg, "magenta")
    
    print()
    # if 13 files are healthly print in green
    expected = 13
    if healthly_counter == expected:
        # print with green background
        cprint(f"{healthly_counter}/{expected} All files are healthly", on_color="on_green", attrs=["bold"])
        
    else:
        cprint(f"{healthly_counter}/{expected} Not all files are healthly", on_color="on_yellow", attrs=["bold"])

    
if __name__ == "__main__":
    main()
    
    # sleep_for = 30
    # while True:
    #     os.system('cls' if os.name == 'nt' else 'clear')
    #     try:
    #         main()
    #     except Exception as e:
    #         print(e)
        
    #     print(f"sleeping for {sleep_for} seconds")
    #     time.sleep(sleep_for)
