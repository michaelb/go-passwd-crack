#!/usr/bin/python3
"""first and foremost, i would like to apologize to everyone including me, reading this code.
It's my first time doing gui things and comments are as sparse as my knowledge of the subject"""
import getpass
from wrapper import *
import os
import threading
import subprocess


from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
from tkinter.ttk import *

from time import sleep

WINDOW_SIZE = "1000x700"


def err_mesage(message):
    messagebox.showerror("Error", message)


def main_window():
    window = Tk()
    window.title("Demo of cracking password files")
    window.geometry(WINDOW_SIZE)

    lbl1 = Label(window, text="Let's get started!", font=("Arial", 20))
    lbl1.grid(column=0, row=0)

    lbl8 = Label(
        window, text="A little bit of culture before we start. It's short, I promise.\n Authentification process of a server (also applies to 'virtual servers' that are more common):\n So you are connecting to a server and like 'hello, this is john'.\n But as anybody could say 'hello this is john', the server is asking you for a password.\n Great. But how does the server knows that password is john's password?. He has to store it and compare it\n to the one 'john' just sent, right? \n\n Not so fast. That would mean the server contains a 'plain text file' with all the users's names and passwords?\n So anybody who could get that file would have, like, access to your account \n(and to your files that are usually encrypted thanks to your password)? \n Moreover, let's not lie to me, you use the same username and password on other \nwebsites/servers right?\n\n That's why the server must use what's called a hash. It's like a mixer function, \nyou give your password 'admin' and it returns \na hash looking like this '2sA./cjnHU6GMjzn84/znD24FSsd'. There is no way to \nguess what john's password is from the hash, and to authentificate john, we just have to ask for the \npassword, 'mix' it and compare the hash to the hash stored in the server. And that's it.\n No password stored in the server.\n\n So you think you are secure now. Only you have your password 'admin' right? \n Well yes, but actually no.\n\nWait wait wait, I just said there was no way to reverse the hash. Well there is no way\n to guess the password directly from the hash, but \n what if someone tried to 'mix' (the same way the servers do) all the passwords they could think of, and then comparing that to your hash?\n I mean, if they have that file with all the user's hashes, they can try as many times as they want.\n At the end of the day, they would obviously try 'admin',(ho, same hash!) they get john's password (and then all of the \ndata stored in those servers + the ones where john use the same password).\n And they will have the password just like that.\n\n You should always use password an attacker wouldn't think of, then. Basically,\n a long word with strange symbols that doesn't mean anything. This very simple programm coded \nby a 19-years old student with 1 year practical experience in coding \n, with your help, show you how easily a weak password is found with this method. ")
    lbl8.grid(column=0, row=1)

    # buttons to choose whether to create a new user

    btn1 = Button(window, text="create new user",
                  command=lambda: windows1bis(window))
    btn1.grid(column=0, row=2)

    btn2 = Button(window, text="use existing password file",
                  command=lambda: use_exitingpassfile(window))
    btn2.grid(column=0, row=3)

    # txt = Entry(window, width=10)
    # txt.grid(column=2, row=1)

    window.mainloop()


def use_exitingpassfile(window):
    window.filename = filedialog.askopenfilename(
        initialdir="~", title="Select password file", filetypes=(("all files", "*"),))
    messagebox.showinfo(
        'Getting the file', "if you could not select the file, you can also place it in your home directory, named 'passwordfile' without the quotes (before clicking ok). Else just go on")

    password_file_path = str(window.filename)
    command = "cp " + password_file_path + " ~/passwordfile"
    os.system(command)
    window.destroy()
    window2(password_file_path)


def windows1bis(window):
    user2create = simpledialog.askstring(
        "username?", "(linux usernames are restricted to a-z characters)")
    password2create = simpledialog.askstring(
        "password?", "accepted symbols:a-z,A-Z,0-9 , 3 letters minimum")
    hash_type = simpledialog.askstring(
        "security?", " you can choose hash functions between 'md5' (legacy, fast to crack) and 'sha512', new standard")
    if "md5" in hash_type:
        hash_type = "1"
    if "sha" in hash_type or "512" in hash_type:
        hash_type = "6"
    if hash_type != "6" and hash_type != "1":
        messagebox.showinfo(
            "Mistyped?", "Looks like you mistyped.I will use sha512 by default")
    if hash_type != "1":
        hash_type = "6"

    os.system("rm ./passwordfile")
    command = "echo " + user2create + \
        ":$(echo " + password2create + \
        " | openssl passwd -" + hash_type + " -stdin ):>> ~/passwordfile"

    os.system(command)

    unixuser = getpass.getuser()
    with open('/home/'+unixuser+'/passwordfile', "r") as f:
        messagebox.showinfo("your hashed password", f.readlines(
        )[-1]+"\n\nand this is actually how users are recorded in servers!\n(this is you)\n(there is even more info when creating a real user but we don't care about that)")
    window.destroy()
    window2("~/passwordfile")


def window2(path=""):
    window = Tk()
    window.geometry(WINDOW_SIZE)
    window.title("Demo of cracking password files")

    if path == "" or '()':
        unixuser = getpass.getuser()
        path = "/home/" + unixuser + "/passwordfile"
        print(path)
    userlist = open_this_file(path)
    if len(userlist) == 0:
        err_mesage("The file provided is empty")

    user_list_name = [parse_text(line, ":")[0] for line in userlist]
    print(user_list_name)
    user = select_user(userlist)

    lbl2 = Label(
        window, text="Select the user whose password you want to crack")
    lbl2.grid(column=0, row=0)

    combo = Combobox(window)
    combo['values'] = tuple(user_list_name)
    combo.current(0)
    combo.grid(column=1, row=0)

    # attack method
    lbl7 = Label(window, text="Select the attack method")
    lbl7.grid(column=0, row=2)
    atk_method = StringVar()
    rad1 = Radiobutton(window, text="bruteforce",
                       value="bruteforce", variable=atk_method)
    rad2 = Radiobutton(window, text="dictionnary",
                       value="dictionnary", variable=atk_method)
    rad1.grid(column=1, row=2)
    rad2.grid(column=1, row=3)

    # alphabet choice
    lbl8 = Label(window, text="Select the alphabet (no effect in dictionnary)\n(note; an attacker usually don't know what to search for\n and will run all these concurrently, but you can give me a hint\n. This program do not support special characters, but you can guess it's even more difficult (=slow) to crack")
    lbl8.grid(column=0, row=5)
    alphabet = StringVar()
    rad6 = Radiobutton(window, text="a-z",
                       value="1", variable=alphabet)
    rad5 = Radiobutton(window, text="a-z,0-9",
                       value="2", variable=alphabet)
    rad4 = Radiobutton(window, text="a-z,A-Z,0-9",
                       value="3", variable=alphabet)
    rad4.grid(column=1, row=6)
    rad5.grid(column=1, row=7)
    rad6.grid(column=1, row=8)

    lbl9 = Label(
        window, text=" Include username in dictionnary combinations? (no effect in bruteforce)")
    lbl9.grid(column=0, row=9)

    username_dictionnary = StringVar()
    rad8 = Radiobutton(window, text="Yes", value="Yes",
                       variable=username_dictionnary)
    rad9 = Radiobutton(window, text="No", value="No",
                       variable=username_dictionnary)
    rad8.grid(column=1, row=11)
    rad9.grid(column=1, row=10)

    global user2crack
    btn2 = Button(window, text="Ok",
                  command=lambda: getuser(combo, window, userlist, user_list_name, atk_method, alphabet, username_dictionnary))
    btn2.grid(column=1, row=18)
    window.mainloop()


def getuser(combo, window, userlist, user_list_name, atk_method, alphabet, username_dictionnary):
    user2crack = combo.get()
    window.destroy()
    window3(user2crack, userlist, user_list_name,
            atk_method.get(), alphabet.get(), username_dictionnary.get())


def launch_crack(salt, checksum, alphabet, attack_type="bruteforce", hash_type="6", username="_"):
    os.system("rm -f status.txt")
    os.system("touch status.txt")
    nb_thread = os.cpu_count()
    if nb_thread == None or nb_thread == 1:
        nb_thread == 1
    else:
        nb_thread = nb_thread - 1
    nb_thread = min(nb_thread, max(len(alphabet), 26))
    print("running on ", nb_thread, " threads")
    # ^in order not to use 100% of the machine's cpu, could cause crashes

    if checksum[-2:] == "\n":
        checksum = checksum[-2]
    if attack_type == "bruteforce":
        command = "./" + attack_type + " " + salt + " " + \
            checksum + " " + alphabet + " " + hash_type + \
            " " + str(nb_thread) + " > ./status.txt "
        os.system(command)

    if attack_type == "dictionnary":
        os.system("split -d -a 2 -n l/" + str(nb_thread) + " dictionnary.txt")
        os.system("mv x* ~/")
        dictionnary_path = "/home/" + getpass.getuser() + "/"
        command = "./" + attack_type + " " + salt + " " + \
            checksum + " " + dictionnary_path + " " + hash_type + \
            " " + str(nb_thread) + " " + username + " > status.txt "
        # os.system(command)
        subprocess.call(command, shell=True)


def window3(user2crack, userlist, user_list_name, atk_method, alphabet, username_dictionnary):
    window = Tk()
    window.geometry(WINDOW_SIZE)
    window.title("Demo of cracking password files")

    for username, line in zip(user_list_name, userlist):
        if username == user2crack:
            line_of_password_file2crack = line
            break
    username, salt_and_hash = deconstruct(line)
    salt, checksum, hash_type = deconstruct_hash(salt_and_hash)
    window.destroy()

    # padding first character, help to simplify task distribution for the backend
    if alphabet == "1":
        alphabet = "+etaoinshrdlcumwfgypbvkjxqz"
    if alphabet == "2":
        alphabet = "+etaoinshrdlcumwfgypbvkjxqz0123456789"
    if alphabet == "3":
        alphabet = "+ETAOINSHRDLCUMWFGYPBVKJXQZetaoinshrdlcumwfgypbvkjxqz0123456789"
    print(alphabet)

    # if "yes" include non-empty username to provide to dictionnary

    if "no" in username_dictionnary:
        username = "_"

    # start crack in new thread
    threads = []
    crack_thread = threading.Thread(
        target=launch_crack, args=(salt, checksum, alphabet, atk_method, hash_type, username))
    threads.append(crack_thread)
    crack_thread.start()
    window4()


def read_status_file():
    global status_of_crack
    with open("./status.txt", "r") as f:
        lines = f.readlines()
    status_of_crack = "".join(lines)
    if "found" in status_of_crack:
        killbackend()
    label_status = Label(
        window_status, text=status_of_crack)
    label_status.grid(column=0, row=2)

    window_status.after(1000, read_status_file)


def killbackend():
    os.system("killall bruteforce &> /dev/null")
    os.system("killall dictionnary &> /dev/null")

    if "killed" in status_of_crack:
        os.system("echo killed >> ./status.txt")


def open_recap():
    os.system("xdg-open recap.txt")


def remove_password():
    os.system("rm -f ~/passwordfile")


def remove_junk():
    os.system("rm -f ~/dictionnary.txt")
    for x in range(10):
        for y in range(10):
            junk = "x"+str(x)+str(y)
            os.system("rm -f ~/"+junk)


def window4():
    global window_status
    window_status = Tk()
    window_status.geometry(WINDOW_SIZE)
    window_status.title("Demo of cracking password files")
    lbl3 = Label(
        window_status, text="If the program is stil running, closing this windows could fail to stop it.\n Use the kill button, or else type\n 'killall bruteforce && killall dictionnary' (without the quotes) in a terminal", justify="center")
    lbl3.grid(column=1, row=5)

    lbl4 = Label(
        window_status, text="status of the programm")
    lbl4.grid(column=0, row=1)
    lbl9 = Label(
        window_status, text="So: when are you safe? You can think so when an attacker,\n even with the help of an optimized program (not like this one)\n and a great amount of computing power, would need a hundreds of years or so to\n crack your password. But don't worry, there is plentiful of other security issues.\n You have just plugged one hole :-) ", justify="center")
    lbl9.grid(column=0, row=3)

    btn3 = Button(window_status, text="Kill background process (if too long)",
                  command=killbackend)
    btn3.grid(column=1, row=10)

    btn4 = Button(window_status, text="Show recap & estimated crack time table",
                  command=open_recap)
    btn4.grid(column=0, row=10)

    btn5 = Button(window_status, text="Remove password file from home?\n You should do that unless you want to keep it",
                  command=remove_password)
    btn5.grid(column=0, row=11)

    btn6 = Button(window_status, text="Remove junk and temp files ?\n Click that once you are finished or it\n could mess up the next try",
                  command=remove_junk)
    btn6.grid(column=0, row=12)

    window_status.after(1000, read_status_file)

    global label_status
    label_status = Label(
        window_status, text=status_of_crack)
    label_status.grid(column=0, row=2)
    window_status.mainloop()


main_window()
