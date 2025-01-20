# DO NOT EDIT THE FOLLOWING LINES
# COURSE CPSC 217 July 2024
# INSTRUCTOR: Jonathan Hudson
# Vqb4blV7487iRCgNdqhs
# DO NOT EDIT THE ABOVE LINES


# Name: Fredella Pang
# UCID: 30247875
# Description:
"""Recieve a file through the command line, and uses the contact lists within to identify relationship between
individuals to categorize patient zero(s), potential zombies, the tastiest and the most viral. It also deduced the height
of individuals away from potential zombies based on their contact lists.
"""

from formatList import *
import sys
from os.path import exists
from colorama import Fore

# CONSTANTS:
FIRSTARGV = 1
FIRSTARGV_LEN = 2

def main():
    """
    Main, gets filename from command line argument (or prompts if not included), reads file into dictionary, then executes contact list categorization
    :return: None
    """
    filename = ""
    # Check args, if there is an argument from the command line, get filename or exit
    if len(sys.argv) > FIRSTARGV:
        # Get filename
        filename = sys.argv[FIRSTARGV]
        if not exists(filename) and len(sys.argv) > FIRSTARGV_LEN:  # multiple arguments, but first argument is not a file
            print(f"{Fore.RED}Your first argument does not seem to be a file that exists.")
            arguments = True # checks whether there are more arguments to be checked
            while arguments:
                for i in range(len(sys.argv) - FIRSTARGV_LEN):  # check all arguments to see if they are a file
                    if exists(sys.argv[i + FIRSTARGV_LEN]):  # if another argument is file, use that
                        filename = sys.argv[i + FIRSTARGV_LEN]
                        print(f"But it seems that argument {i + FIRSTARGV_LEN} is a file that exists{Fore.LIGHTWHITE_EX}")
                        arguments = False
                    if arguments and i == (len(sys.argv) - FIRSTARGV_LEN - FIRSTARGV):   # when at last file and no file exist --> exit
                        print (f"Sorry, none of the arguments are a file that exists.{Fore.LIGHTWHITE_EX}")
                        exit()
        elif not exists(filename):  # no file exist so exit
            exit(f"{Fore.RED}Sorry your file does not exist{Fore.LIGHTWHITE_EX}")
        elif len(sys.argv) > (FIRSTARGV_LEN): # first argument is a file that exist, but there are too many arguments
            print(f"{Fore.BLUE}Too many arguments. But that's okay because it seems that your first argument is a file that exists....{Fore.LIGHTWHITE_EX}")
    else:  # No argument is entered in the cmd line so get input filename
        file_inputted = False
        while not file_inputted:
            filename = input(f"{Fore.BLUE}Oops no filename provided. Enter filename: {Fore.LIGHTWHITE_EX}")
            if exists(filename):
                file_inputted = True

    # Open, read and close file
    file = open(filename)
    data = file.read()
    file.close()

    # Turn file into a list
    data = data.splitlines()  # create a list that separates items per line (\n)
    for i in range(len(data)):  # for every item in list
        data[i] = data[i].split(",")  # split each comma separated name
    data = (sorted(data))
    # Make dict from file
    names_dict = {}
    for contact in data: # for each contact list
        key = contact[0]  # key is first name of contact list
        contact.pop(0)  # remove key from contact list
        names_dict[key] = contact  # add contact list to the person/key
    # Part 1
    # Print data from dict
    print("Contact Records: ")
    for keys in names_dict.keys():  # For each name with a contact list
        contacts = formatList(names_dict[keys])
        print("\t", keys, "had contact with", contacts)  # print name + "had contact with" + contacts

    # Part 2
    # list_p2 = part2(dict)
    list_p2 = part2(names_dict)
    # print(part 2 header + formatList(list_p2))
    print("\n"+"Patient Zero(s): ", formatList(list_p2))

    # Part 3
    # list_p3 = part3(dict)
    list_p3 = part3(names_dict)
    # print(part 3 header+formatList(list_p3))
    print("Potential Zombies: ", formatList(list_p3))

    # Part 4
    # list_p4 = part4(dict)
    list_p4 = part4(names_dict)
    # print(part 4 header+formatList(list_p4))
    print("Neither Patient Zero or Potential Zombie: ", formatList(list_p4))

    # Part 5
    # list_p5 = part5(dict)
    list_p5 = part5(names_dict)
    # print(part 5 header+formatList(list_p5))
    print("Most Viral: ", formatList(list_p5))

    # Part 6
    # list_p6 = part6(dict)
    list_p6 = part6(names_dict)
    # print(part 6 header+formatList(list_p5))
    print("Tastiest: ", formatList(list_p6))

    # Part 7
    # print(part 7 header)
    print("\nHeights: ")
    # p7_dict = part7
    height_dict = part7(names_dict, filename)
    # print(names + ":" + height)
    for names in height_dict.keys():
        print("\t" + names + ":", height_dict[names])

    # Bonus Header
    print("\n"+"_"*60)
    print("BONUS".center(60, "*"))

    # Part B1
    list_b1 = partb1(names_dict)
    # print(part b1 header+formatList(list_b1))
    print("Spreader Zombie: ", formatList(list_b1))

    # Part B2
    list_b2 = partb2(names_dict)
    # print(part b2 header+formatList(list_b2))
    print("Regular Zombie: ", formatList(list_b2))

    # Part B3
    list_b3 = partb3(names_dict)
    # print(part b3 header+formatList(list_b3))
    print("Zombie Predators: ", formatList(list_b3),"\n")


def notkeys_list(my_dict):
    """
    Description: Get the names who are contacts in contact lists.
    :param my_dict: dictionary sorting contact lists of individuals in the file
    :return: list of individual names present within contact lists
    """

    notkeys_dict = {}
    nklist = []

    for key in my_dict.keys():
        for notkey in my_dict[key]:
            notkeys_dict[notkey] = notkey
    nklist = list(notkeys_dict.keys())
    return nklist


def part2(my_dict):
    """
    Description: Get the names of patient zero(s)
    :param my_dict:dictionary sorting contact lists of individuals in the file
    :return: list of individuals that do not appear in contact lists of other individuals
    """
    list = []  # create list

    for key in my_dict.keys():  # for every person with a contact list
        if key not in notkeys_list(my_dict):  # if they don't appear in list of people within contact lists
            list.append(key)  # append name in list
    return list


def part3(my_dict):
    """
    Description: Get the names of potential zombies
    :param my_dict:dictionary sorting contact lists of individuals in the file
    :return: list of individuals that appear in contact lists but do not have contact lists themselves
    """
    list = []  # create list

    for name in notkeys_list(my_dict):  # for every person within a contact list
        if name not in my_dict.keys():  # if they do not have their own contact list
            list.append(name)  # append name in list
    return list


def part4(my_dict):
    """
    Description: Get the names of individuals who are not potential zombies nor patients zeros
    :param my_dict:dictionary sorting contact lists of individuals in the file
    :return: list of individual who are neither potential zombies nor patient zero(s)
    """
    list = []  # create list

    for name in notkeys_list(my_dict):  # for every person within a contact list
        if name not in part3(my_dict):  # if they are not a potential zombie (they have a contact list)
            list.append(name)  # append name in list
    return list


def part5(my_dict):
    """
    Description: Get the names of the most viral individuals
    :param my_dict:dictionary sorting contact lists of individuals in the file
    :return:a list of individuals who had the longest contact lists
    """
    list = []  # create main list
    len_list = []  # create list of contact list lengths
    len_dict = {}  # create list to keep track of {list position: name}

    count = 0  # to count list position
    for key in my_dict.keys():  # for every person with a contact list
        len_list.append(len(my_dict[key]))  # append the length of their contact list to len_list
        len_dict[count] = key  # add {list position: name of person} to len_dict
        count += 1  # counter += 1
    max_len = max(len_list)  # find the value of the longest contact list
    for i in range(len_list.count(max_len)):  # for every value that is the longest contact list
        list.append(len_dict[len_list.index(max_len)])  # append the name that belongs to the first occurence of the max length
        len_list[len_list.index(max_len)] = 0  # change their length to 0, allow for loop to reach next occurence of max length
    return list


def part6(my_dict):
    """
    Description: Get the names of the tastiest individuals
    :param my_dict:dictionary sorting contact lists of individuals in the file
    :return: list of individuals who appeared in the most contact lists
    """
    list = []  # create the main list
    count_list = []
    count_dict = {}

    key_count = 0  # counter of position of contact name in lsit
    for contact in notkeys_list(my_dict):  # for every person within a contact list (contact)
        num_count = 0  # counter of times contact is in a contact list
        for item in my_dict.keys():  # for every person with a contact list (key)
            # check every item in my_dict
            if contact in my_dict[item]:  # if contact is in the contact list of key
                num_count += 1
        count_list.append(num_count)  # append number of times contact is in a contact list
        count_dict[key_count] = contact  # add {list position: contact name}
        key_count += 1
    max_num = max(count_list)  # find the person with the most occurences in other contact lists
    for i in range(count_list.count(max_num)):  # for i in range (occurence of the max number)
        list.append(count_dict[count_list.index(max_num)])  # append the name that belongs to the first occurence of the max number
        count_list[count_list.index(max_num)] = 0  # change their length to 0, allow for loop to reach next occurence of max length
    return list
def part7(my_dict, filename):
    """
    Description: Get the heights of individuals
    :param my_dict:dictionary sorting contact lists of individuals in the file
    :param filename: filename of the contact lists
    :return: dictionary sorting the heights of individuals in the file
    """
    # create a flat list with all names from the file
    file = open(filename)  # open file
    allpeople = file.read()  # get names from file
    file.close()  #close file
    allpeople = allpeople.splitlines()  # create a list that separates items per line (\n)
    for i in range(len(allpeople)):  # for every item in list
        allpeople[i] = allpeople[i].split(",")  # split each comma separated name
    allpeople = sum(allpeople, [])  # sum list together to get unified and flat list with all names

    # use unfiltered list to create a filtered list with no repeats
    people = []
    for person in allpeople: # for all names in unfiltered list
        if person not in people:  # if name is not already in the filtered list
            people.append(person)  # append new person

    # create a dictionary to store people name with their height
    height_dict = {}
    for person in people: # for all people in filtered list
        height_dict[person] = 0  # add their names to the height_dict and set their heights to 0

    # define the distance from potential zombies
    changed = True  # set changed to True
    while changed:  # == True  # while something has changed
        changed = False  # set changed to False
        for p1 in my_dict.keys():  # for each person, p1, who has a contact list
            for p2 in my_dict[p1]:  # for each person, p2, who is in p1's contact list
                if height_dict[p1] <= height_dict[p2]: # if the height of p1 is <= to the height of p2
                    height_dict[p1] = height_dict[p2] + 1  # set the height of p1 to the height of p2 + 1
                    changed = True  # set changed to True
    return height_dict


def partb1(my_dict):
    """
    Description: Get the spreader zombies
    :param my_dict:dictionary sorting contact lists of individuals in the file
    :return: list of individuals who only had contact with potential zombies
    """
    list = []
    for key in my_dict.keys():  # check each key
        if len(my_dict[key]) == 1:  # if the key's contact list consist of only one person
            if my_dict[key][0] in part3(my_dict):  # if the contact is a potential zombie
                list.append(key)  # add key's name to the list
    return list

def partb2(my_dict):
    """
    Description: Get the regular zombies
    :param my_dict:dictionary sorting contact lists of individuals in the file
    :return: list of individual who has contact with a potential zombie and another person
    """
    list = []
    for key in my_dict.keys():  # check each key
        if len(my_dict[key]) > 1:  # if contact list is longer than one person
            status = 0  # conditions fulfilled
            count = 0
            repeat = len(my_dict[key])  # number of person in key's contact list
            for i in range(repeat):  # for every person in key's contact list
                if my_dict[key][count] in part3(my_dict):  # condition 1: if contact is a potential zombie
                    status += 1
                    try:
                        if my_dict[key][count+1] not in part3(my_dict):  # condition 2: if another contact is not a potential zombie
                            status += 1
                    except IndexError: # if potential zombie is found at the end of the contact list
                        if my_dict[key][count-1] not in part3(my_dict):
                            status += 1
                if status == 2:  # if both conditions are fulfilled
                    list.append(key)  # add the key's name to the list
                    status = 0 # reset conditions fulfilled counter
                count += 1 # check next person in contact list
    return list

def partb3(my_dict):
    """
    Description: Get the zombie predators
    :param my_dict:dictionary sorting contact lists of individuals in the file
    :return: list of individuals who are not potential zombies, spreader zombies, or regular zombies
    """
    list = []
    list.extend(my_dict.keys())  # put all names into the list
    for key in my_dict.keys():  # check each key
        if key in partb1(my_dict): # if key is a spreader zombie
            list.remove(key) # remove from list
        elif key in partb2(my_dict):  # if key is a regular zombie
            list.remove(key)  # remove from list
    return list

main()