package main

import (
	"bufio"
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"time"
)

func main() {
	var filename string
	if len(os.Args) == 1 {
		fmt.Println("Inferred filename", filepath.Base(os.Args[0]))
		curFile := filepath.Base(os.Args[0])
		filename = fmt.Sprintf("../inputs/%s.txt", curFile)
	} else {
		filename = os.Args[1]
	}
	t0 := time.Now()
	fmt.Printf("Reading from %s,", filename)
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var line string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line = scanner.Text()
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))

	t1 := time.Now()
	var i int

	mb, err := hex.DecodeString("f0")
	if err != nil {
		log.Fatal(err)
	}
	mask := int(mb[0])

outer:
	for i = 0; true; i++ {
		if i%200000 == 0 {
			fmt.Println("iter:", i)
		}
		hash := md5.Sum([]byte(fmt.Sprintf("%s%d", line, i)))
		for _, b := range hash[:2] {
			if int(b) != 0 {
				continue outer
			}
		}
		if int(hash[2])&mask != 0 {
			continue outer
		}
		break
	}
	fmt.Printf("1: %v, %v\n", i, time.Since(t1))

	t2 := time.Now()
outer2:
	for i = 0; true; i++ {
		if i%2000000 == 0 {
			fmt.Println("iter:", i)
		}
		hash := md5.Sum([]byte(fmt.Sprintf("%s%d", line, i)))
		for _, b := range hash[:3] {
			if int(b) != 0 {
				continue outer2
			}
		}
		break
	}
	fmt.Printf("2: %v, %v\n", i, time.Since(t2))
}
