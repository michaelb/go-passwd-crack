#!/usr/bin/python3
import sys
import os
import subprocess
from time import sleep


def open_file():
    List_users = []
    with open(sys.argv[1], "r") as f:
        List_users = f.readlines()

    return List_users


def open_this_file(path):
    List_users = []
    with open(path, "r") as f:
        List_users = f.readlines()

    return List_users


def select_user(List_users, number=-1):
    if len(List_users) == 1:
        return List_users[0]
    if len(List_users) == 0:
        print("The file is empty!", file=sys.stderr)
    # there is more than one user
    return List_users[number]  # by defaut return the last line


def parse_text(text, symbol):
    index = 0
    for i, car in enumerate(text):
        index = i
        if car == symbol:
            word = text[:index]
            rest = text[index + 1:]
            return word, rest
    return text, ""


def deconstruct(line):
    user, line = parse_text(line, ":")
    if user == "" or user == " " or line == "":
        print("The file is not a password file.")
    salt_and_hash, line = parse_text(line, ":")
    return user, salt_and_hash


def deconstruct_hash(salt_and_hash):
    magic_number, salt_and_hash = parse_text(salt_and_hash[1:], "$")
    if magic_number != "6" and magic_number != "1":
        print("User password was not hashed with sha512 or md5 algorithm.\n Only those are supported")
        sleep(1)
    salt, salt_and_hash = parse_text(salt_and_hash, "$")
    checksum, salt_and_hash = parse_text(salt_and_hash, "$")
    return salt, checksum, magic_number


def launcher():
    userlist = open_file()
    user = select_user(userlist)
    username, salt_and_hash = deconstruct(user)
    salt, checksum, magic_number = deconstruct_hash(salt_and_hash)

    alphabet = "abcdefghijklmnopqrstuvxyz"

    command = "./bruteforce " + \
        salt + " " + checksum + " " + alphabet
    #subprocess.call("ls" + " -a")
    os.system(command)
    return 0


if __name__ == '__main__':
    launcher()
