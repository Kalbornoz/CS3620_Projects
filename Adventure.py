from cgitb import text
import time
import sys
import re
import textwrap

my_adventure = open("myAdventure.txt", "w+")
my_choice = 0
choice_num1 = 1
choice_num2 = 2
exit = 0
name = ""


def slow_print(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(.05)


def regexParse(regex_str, text):
    return re.search(regex_str, text)


def resetChoices(regex_str, text):
    if(not text.__contains__("THE END") and not text.__contains__("TO BE CONTINUED")):
        match = regexParse(regex_str, text)
        choice_list = match[0].split(",")
        global choice_num1
        global choice_num2

        choice_num1 = int(choice_list[0])
        choice_num2 = int(choice_list[1])


def getIntro():
    intro = open("Story/Intro.txt", "r")

    for line in intro.readlines():
        my_adventure.write(line + "\n")
        slow_print(line)
    intro.close()


def getChoices(num1, num2):
    print()
    choicefile = open("Story/choices.txt", "r")
    choices = choicefile.readlines()
    for choice in choices[num1 - 1: num2]:
        my_adventure.write("\n" + choice + "\n")
    print()
    slow_print(choices[num1 - 1: num2])

    choicefile.close()


def setExit(txt):
    if(txt.__contains__("THE END") or txt.__contains__("TO BE CONTINUED")):
        global exit
        exit = 1


def getNarrative(num):
    try:
        num = int(num)
    except:
        return
    if(int(num) != choice_num1 and int(num) != choice_num2):
        return
    print()
    narrativefile = open("Story/narratives.txt", "r")
    narratives = narrativefile.read()
    narratives = narratives.replace("<Name>", name)
    narrativefile.close()
    paragraph = regexParse(
        r"({0}:(.|\n)+?(?=\n\n\n))".format(num), narratives)

    resetChoices(r"[0-9]{1,2},[0-9]{1,2}", paragraph[0])
    my_adventure.write(paragraph[0] + "\n")
    slow_print(paragraph[0])
    setExit(paragraph[0])
    if(exit == 0):
        getChoices(choice_num1, choice_num2)


if __name__ == '__main__':
    name = input("Please enter in your name for this adventure: ")
    getIntro()
    getChoices(choice_num1, choice_num2)
    while(exit == 0):
        my_choice = input("What is your choice: ")
        getNarrative(my_choice)
        print()
    my_adventure.close()
