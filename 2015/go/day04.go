package main

import (
	"bufio"
	"crypto/md5"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"time"
)

func findKey(prefix string, mask []int) int {
outer:
	for i := 0; true; i++ {
		hash := md5.Sum([]byte(fmt.Sprintf("%s%d", prefix, i)))
		for i, m := range mask {
			b := hash[i]
			if int(b)&m != 0 {
				continue outer
			}
		}
		return i
	}
	return 0
}

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
	mask := []int{255, 255, 255 - 15} // 0xf0
	i := findKey(line, mask)
	fmt.Printf("1: %v, %v\n", i, time.Since(t1))

	t2 := time.Now()
	mask = []int{255, 255, 255}
	i = findKey(line, mask)
	fmt.Printf("2: %v, %v\n", i, time.Since(t2))
}
