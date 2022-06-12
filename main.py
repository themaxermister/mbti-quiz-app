import os
import sys
import csv
import json

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')


current = {
    "E": 0,
    "I": 0,
    "S": 0,
    "N": 0,
    "T": 0,
    "F": 0,
    "J": 0,
    "P": 0
}

final = {}

def title():
    print("""  __  __ ____ _______ _____    ____        _     
 |  \/  |  _ \__   __|_   _|  / __ \      (_)    
 | \  / | |_) | | |    | |   | |  | |_   _ _ ____
 | |\/| |  _ <  | |    | |   | |  | | | | | |_  /
 | |  | | |_) | | |   _| |_  | |__| | |_| | |/ / 
 |_|  |_|____/  |_|  |_____|  \___\_\\__,_|_/___|

    """)

def menu():
    print("Menu")
    print("-----------------")
    print("(1) Take the quiz")
    print("(2) Show last results")
    print("\n")

def remove_spaces(str_input):
    return str_input.lower().strip().replace(" ", "_")\
    
def check_clarity(num):
    if num < 14:
        return "Slight"
    elif num < 17:
        return "Moderate"
    elif num < 20:
        return "Clear"
    else:
        return "Very clear"

def get_results():
    # Check E/I
    if current["I"] > current["E"]:
        final["I"] = check_clarity(current["I"])
    else:
        final["E"] = check_clarity(current["E"])

    # Check S/N
    if current["N"] >= current["S"]:
        final["N"] = check_clarity(current["N"])
    else:
        final["S"] = check_clarity(current["S"])

    # Check T/F
    if current["F"] >= current["T"]:
        final["F"] = check_clarity(current["F"])
    else:
        final["T"] = check_clarity(current["T"])

    # Check J/P
    if current["P"] >= current["J"]:
        final["P"] = check_clarity(current["P"])
    else:
        final["J"] = check_clarity(current["J"])

    return final

def display_results():
    print("RESULTS:")
    for key, value in final.items():
        print(key, ":", value)
    print("\n")
    input("Press enter to continue")

def append_results(file_name):
    with open(file_name, 'a') as f:
        # Pass this file object to csv.writer()
        # and get a writer object
        writer = csv.writer(f)
    
        # Pass the list as an argument into
        # the writerow()
        writer.writerow([])
        writer.writerow(["Results", "Clarity"])
        for key, value in final.items():
            writer.writerow([key, value])
        #Close the file object
        f.close()

def quiz():
    # Get file name
    csv_file_name = ""

    while True:
        user_name = remove_spaces(input("Enter name: "))
        user_file_name = "%s_results.csv" % user_name
        csv_file_name = os.path.join(get_download_path(), user_file_name)
        confirm_user = input ("Saving results to %s. Confirm (Y/n)? " % (csv_file_name))
        
        if confirm_user.lower() in ["y", ""]:
            break
        elif confirm_user.lower() == "n":
            input("Cancelled. Press enter to try again\n")
        else:
            input("Invalid option. Press enter to try again\n")
    
    os.system('cls' if os.name == 'nt' else 'clear')

    # Start csv writer
    csv_f = open(csv_file_name, 'w')
    writer = csv.writer(csv_f)
    header = ["Question", "Answer", "Result"]
    writer.writerow(header)
    
    # Load Qns
    f = open(resource_path("mbti.json"))
    data = json.load(f)
    for obj in data['form']:
        for key, value in obj.items():
            print_qns = "Question %s: %s" % (key, value['qns'])
            print(print_qns)
            print("-" * (len(print_qns)+1))
            print("Option A:", value["ansA"]["response"])
            print("Option B:", value["ansB"]["response"])
            print("\n")

            ans = ""
            while True:
                ans = input("Chosen option: ")
                if ans.lower() not in ["a", "b"]:
                    input("Invalid option. Press enter to try again\n")
                else:
                    break
        
            row = []
            if ans == "a":
                row = [value['qns'], value["ansA"]["response"], value["ansA"]["result"]]
                current[value["ansA"]["result"]] += 1
            elif ans == "b":
                row = [value['qns'], value["ansB"]["response"], value["ansB"]["result"]]
                current[value["ansB"]["result"]] += 1
            writer.writerow(row)
        
        os.system('cls' if os.name == 'nt' else 'clear')

    csv_f.close()
    f.close()
    get_results()
    display_results()
    append_results(csv_file_name)

def reset():
    current = {
        "E": 0,
        "I": 0,
        "S": 0,
        "N": 0,
        "T": 0,
        "F": 0,
        "J": 0,
        "P": 0
    }

    final = {}

if __name__ == "__main__":
    title()
    input("Press enter to continue")

    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        menu()
        user_input = input("Choose an option: ")
        
        if user_input == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            reset()
            quiz()
        elif user_input == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            if len(final) > 0:
                display_results()
                input()
            else:
                input("No results saved. Press enter to try again\n")
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            input("Invalid option. Press enter to try again\n")
