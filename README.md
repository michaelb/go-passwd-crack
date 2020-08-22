# Password cracker

**This project was made in a week and had learning goals more than final usability, prettiness or quality in general.**

Although this can be used for educational purposes, you should not rely on it to provide you with extremely accurate information, or estimation of your password's strength.

## More info

To compile the go part of the program, a Makefile is provided in crack_passwd: just run 'make' in that directory. (See dependencies first)

To launch the program, just (double) click on the run.sh file.

Features:

- Efficient use of the ressources. This program run on your CPU and use all but one thread.
- Scales up to 26/52/62 threads in bruteforce mode (depending on the length of the alphabet), and up to 100 threads in dictionnary mode.
- GUI fully functional
- Crack password from aA-zZ,0-9, bruteforce limited to 16 characters.

Dependencies:
Openssl (to create new users)
Go to re-compile binaries
A gnu-style make to use the (short) makefile.
Two go libraries to compute hashes. Those can be pulled from the go repos anytime and i have no control over it. Such a problem would appear at compile time.

Troubleshooting:

- Program does not launch, nothing is happening/ just opening the run.sh as text: Check the permissions of run.sh, if it not executable, you should open a terminal, navigate to the directory containing run.sh and type "chmod +x run.sh"
- Program launch but some windows are blank: Are you sure to have selected all the fields? (eg: alphabet for bruteforce). You should read what's onscreen before clicking Ok

- Program is slow after the previous one crashed. You should "kill background process" by clicking on the button. The previous program must still be running. Then start over.

- Other: make sure to run the program as a normal user, with a ~ home directory and access to it.

Who can be intersted by this project? Not many people, hmm. This is not a state-of-the-art solution to hash cracking (better tools exist to do that).

Some avantages of this project are:

- reasonably fast operation
- educative vision: short text messages explaining the how and why
- works with real password files _and_ the fake ones the program can generate

WIP:

- proper thread communication and result returning
