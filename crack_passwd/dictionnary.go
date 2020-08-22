package main

import (
	"fmt"
	"github.com/kless/osutil/user/crypt/md5_crypt"
	"github.com/kless/osutil/user/crypt/sha512_crypt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

var password_found string = ""

func crack(salt, checksum, hash_type, path, username string) string {
	//compare hash of all (salt+) passwords of length <length>  to given checksum
	file, err := os.Open(path)
	_ = err
	b, err2 := ioutil.ReadAll(file)
	_ = err2

	s := string(b)
	purged := strings.Fields(s)
	password2 := ""

	for _, password := range purged {
		if hash_type == "6" {
			if hash_sha512(salt, password) == checksum {
				fmt.Printf("\n\npassword found: %v\n\n", password)
				return password
			}
		}
		if hash_type == "1" {
			if hash_md5(salt, password) == checksum {
				fmt.Printf("\n\npassword found: %v\n\n", password)
				return password
			}
		}
		if username != "_" {
			password2 = username + password
			if hash_type == "6" {
				if hash_sha512(salt, password2) == checksum {
					fmt.Printf("\n\npassword found: %v\n\n", password2)
					return password2
				}
			}
			if hash_type == "1" {
				if hash_md5(salt, password2) == checksum {
					fmt.Printf("\n\npassword found: %v\n\n", password2)
					return password2
				}
			}

		}
	}
	fmt.Printf("no password found on this thread\n")
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

func main() {
	fmt.Println("running")
	salt := os.Args[1]
	checksum := os.Args[2]
	dictionnary := os.Args[3] //contain the :path to the chunks of dictionnary
	hash_type := os.Args[4]

	nb_thread, err := strconv.Atoi(os.Args[5])
	username := os.Args[6]

	_ = err

	nb := ""
	path := ""
	if username != "_" {
		fmt.Println("also searching for combinations with username: ", username)
	}

	for thread := 0; thread < nb_thread; thread++ {
		nb = strconv.Itoa(thread)
		if len(nb) == 1 {
			nb = "x0" + nb
		} else {
			nb = "x" + nb
		}
		path = dictionnary + nb
		go crack(salt, checksum, hash_type, path, username)
	}

	for {
		time.Sleep(1000)
	}

}
