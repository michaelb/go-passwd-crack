package main

import (
	"fmt"
	"github.com/kless/osutil/user/crypt/md5_crypt"
	"github.com/kless/osutil/user/crypt/sha512_crypt"
	"os"
	"strconv"
	"time"
)

var password_found string = ""

func next_symbol(old_symbol string, alphabet string) string {
	//return the next symbol in the alphabet and nothing if the old_symbol is the last
	var prev_symbol string = ""
	for i, symbol := range alphabet {
		if prev_symbol == old_symbol {
			return string(symbol)
		}
		prev_symbol = string(symbol)
		_ = i
	}
	return ""
}

func next_password(password, alphabet string, length int) string {
	//update (recursively, clock-style) the given password to the following password in alphabetical order
	if len(password) == 0 {
		return ""
	}
	last_char := password[len(password)-1:]
	new_char := next_symbol(last_char, alphabet)
	if new_char == "" {
		return next_password(password[:len(password)-1], alphabet, length)
	} else {
		password = password[:len(password)-1] + new_char
	}
	for start_of_alphabet := string(alphabet[0]); len(password) < length; {
		password += start_of_alphabet
	}
	return password
}

func crack(salt, checksum, alphabet, password_start, password_stop string, length int, hash_type string) string {
	//compare hash of all (salt+) passwords of length <length>  to given checksum
	password := password_start
	for password != "" {
		password = next_password(password, alphabet, length)
		if hash_type == "6" {
			if hash_sha512(salt, password) == checksum {
				fmt.Println(password)
				return password
			}
		}
		if hash_type == "1" {
			if hash_md5(salt, password) == checksum {
				fmt.Println(password)
				return password
			}
		}
		if len(password) > 0 && len(password_stop) > 0 {
			if password[0] == password_stop[0] {
				break
			}
		}
	}
	return ""
}

func hash_sha512(salt, password string) string {
	c := sha512_crypt.New()
	hash, err := c.Generate([]byte(password), []byte("$6$"+salt))
	if err != nil {
		panic(err)
	}
	return hash[len(salt)+4:]
}

func hash_md5(salt, password string) string {
	c := md5_crypt.New()
	hash, err := c.Generate([]byte(password), []byte("$1$"+salt))
	if err != nil {
		panic(err)
	}
	return hash[len(salt)+4:]
}

func launch(salt, checksum, global_alphabet, password_start, password_stop string, max_length, thread int, hash_type string) {
	pass_found := ""
	for length := 1; pass_found == "" && length <= max_length; length++ {
		pass_found = crack(salt, checksum, global_alphabet, password_start, password_stop, length, hash_type)

		if pass_found != "" {
			fmt.Println("\n\npassword found: ", pass_found, "\nyou can kill the background process")
		}
	}
	fmt.Println("thread ", thread, ":no password_found")
}

func main() {
	fmt.Println("running")
	salt := os.Args[1]
	checksum := os.Args[2]
	global_alphabet := os.Args[3]
	hash_type := os.Args[4]

	nb_thread, err := strconv.Atoi(os.Args[5])
	_ = err

	max_length := 16
	l := len(global_alphabet)
	password_start := ""
	password_stop := ""
	for thread := 0; thread < nb_thread; thread++ {
		password_start = string(global_alphabet[l*thread/nb_thread])
		if thread != nb_thread-1 {
			password_stop = string(global_alphabet[l*(thread+1)/nb_thread])
		} else {
			password_stop = ""
		}
		go launch(salt, checksum, global_alphabet, password_start, password_stop, max_length, thread, hash_type)
	}
	for {
		time.Sleep(1000)
	}

}
