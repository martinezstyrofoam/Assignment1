"""
CP1404 Assignment 1 - Travel Tracker
Name: Siron Tommy Aban
Date started: 27/10/24
GitHub URL: https://github.com/martinezstyrofoam/Assignment1
"""
import random
def main():
    """..."""
    choice, menu = intro()

    p_country, p_locale, p_open, p_priority, p_visited = data_load()

    menu_loop(choice, menu, p_country, p_locale, p_priority, p_visited)
    data_save(p_country, p_locale, p_open, p_priority, p_visited)
    print("Have a nice day ( •̀ᴗ•́ )و")


def intro():
    welcome = """Welcome to Siron Tommy Martinez's Travel Tracker!"""
    menu = """
    D - Display all places
    R - Recommend a random place
    A - Add a new place
    M - Mark a place as visited
    Q - Quit
    """
    print(welcome)
    print(menu)
    choice = input(">>> ").upper()
    return choice, menu


def data_save(p_country, p_locale, p_open, p_priority, p_visited):
    p_write = open("places.csv", "w")
    for i, x in enumerate(p_locale):
        p_write.write(f"{p_locale[i]}, {p_country[i]}, {p_priority[i]},{p_visited[i]}\n")
    p_write.close()
    p_open.close()

# Menu loop which allows the user to continuously use the code until they are finished with it.
def menu_loop(choice, menu, p_country, p_locale, p_priority, p_visited):
    while choice != "Q":

        if choice == "D":
            display(p_country, p_locale, p_priority, p_visited)

        elif choice == "R":
            recommend(p_country, p_locale, p_priority, p_visited)

        elif choice == "A":
            addition(p_country, p_locale, p_priority, p_visited)

        elif choice == "M":
            mark_visited(p_country, p_locale, p_priority, p_visited)
        else:
            print("Invalid menu choice.")
        print(menu)
        choice = input(">>> ").upper()

# Uses copy of code from display but rather than taking from combined list, it just gets it raw data files.
def mark_visited(p_country, p_locale, p_priority, p_visited):
    for i, x in enumerate(p_locale):
        if p_visited[i] == "n":
            v_aster = "*"
        else:
            v_aster = " "
        print(f"{v_aster} {i + 1}. {p_locale[i]:9} in {p_country[i]:11}{p_priority[i]:>3}")
    print(f"{len(p_visited)} places tracked. You still want to visit {p_visited.count('n')}")
    p_mark_number = input("Enter the number of a place you want to mark as visited: ").strip()

    if p_mark_number.isdigit():
        index = int(p_mark_number) - 1  # Index is supposed to be tracked from 0, code fixes it.
        if 0 <= index < len(p_locale):
            p_visited[index] = 'v'
            print(f"{p_locale[index]} in {p_country[index]} has been marked as visited.")
        else:
            print("Invalid number. Please select a valid place from the list.")
    else:
        print("Input must be a whole number.")

# Adds a new location.
def addition(p_country, p_locale, p_priority, p_visited):
    p_locale_add = input("Name: ").strip()

    # Error-checking for name
    while len(p_locale_add) == 0:
        print("Input cannot be blank.")
        p_locale_add = input("Name: ").strip()

    # Error-checking for country
    p_country_add = input("Country: ").strip()
    while len(p_country_add) == 0:
        print("Input cannot be blank.")
        p_country_add = input("Country: ").strip()

    # Error-checking for priority
    p_priority_add = input("Priority: ").strip()
    p_priority_valid = False
    while p_priority_valid == False:
        p_priority_valid = p_priority_add.isdigit()

        if p_priority_valid == True:
            p_priority_valid = int(p_priority_add) > 0

        if p_priority_valid == False:
            if not p_priority_add.isdigit(): # Accounts if user puts in a float.
                print("Input must be a whole number.")
            else: # Incase they're smart enough to put a number in but it's too small.
                print("Number must be greater than 0.")
            p_priority_add = input("Priority: ").strip()

    # Adds to the list, not the file
    p_locale.append(p_locale_add)
    p_country.append(p_country_add)
    p_priority.append(p_priority_add)
    p_visited.append('n') # Marks new locations as not vistied
    print(f"{p_locale_add} in {p_country_add} (priority {p_priority_add}) has been added to Travel Tracker.")


def recommend(p_country, p_locale, p_priority, p_visited):
    p_unvisited = []
    for i, x in enumerate(p_locale):
        if p_visited[i].strip().lower() == 'n': # makes a list of unvisited places to call back to.
            p_unvisited.append((p_locale[i], p_country[i], p_priority[i]))
    if len(p_unvisited) > 0: # uses said list to select randomly from the list of unvisited locations.
        r_index = random.randint(0, len(p_unvisited) - 1)
        r_place = p_unvisited[r_index]
        print(f"How about... {r_place[0]} in {r_place[1]}?")
    else:
        print("No places left to visit!")

# Displays the list of countries, their locales to visit, whether they've been visited, and priority.
def display(p_country, p_locale, p_priority, p_visited):
    combined_data = []
    for i, x in enumerate(p_locale):
        combined_length = len(p_locale[i]) + len(p_country[i])
        combined_data.append((combined_length, p_locale[i], p_country[i], p_priority[i], p_visited[i])) # adds combined data to new list so it can sort
    for i, x in enumerate(combined_data):
        for j in range(0, len(combined_data) - i - 1): # zero index acc for
            if combined_data[j][0] > combined_data[j + 1][0]:
                combined_data[j], combined_data[j + 1] = combined_data[j + 1], combined_data[j]
    for i, x in enumerate(combined_data):
        v_aster = "*" # Puts an asterisk if they have been visited.
        if x[4] == "v":
            v_aster = " "
        print(f"{v_aster} {i + 1}. {x[1]:9} in {x[2]:11}{x[3]:>3}")
    print(f"{len(p_visited)} places tracked. You still want to visit {p_visited.count('n')}")

# Responsiblke for opening and retrieving the data for Python.
def data_load():
    p_open = open("places.csv", "r")
    p_read = p_open.readlines()
    p_country, p_locale, p_priority, p_visited = lists(p_read)
    return p_country, p_locale, p_open, p_priority, p_visited


def lists(p_read):
    p_locale = []
    p_country = []
    p_priority = []
    p_visited = []
    # Transfers data from CSV file into the lists.
    for x in p_read:
        row = x.strip().split(",")
        p_locale.append(row[0].strip())
        p_country.append(row[1].strip())
        p_priority.append(row[2].strip())
        p_visited.append(row[3].strip())
    return p_country, p_locale, p_priority, p_visited


if __name__ == '__main__':
    main()
