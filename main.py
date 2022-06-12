import os
import sys
import json

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

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
    
def quiz():
    f = open(resource_path("mbti.json"))
    data = json.load(f)
    for obj in data['form']:
        for key, value in obj.items():
            print("Question", key)
            print("-----------")
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
        
            if ans == "a":
                current[value["ansA"]["result"]] += 1
            elif ans == "b":
                current[value["ansB"]["result"]] += 1
        
        os.system('cls' if os.name == 'nt' else 'clear')

    get_results()
    display_results()

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
