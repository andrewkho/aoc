package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"
	"time"
)

func step(cur string) string {
	left := 0
	nxt := []string{}
	for left < len(cur) {
		v := cur[left]
		right := left + 1
		for right < len(cur) && cur[right] == v {
			right++
		}
		nxt = append(nxt, fmt.Sprintf("%d", right-left))
		nxt = append(nxt, string(v))
		left = right
	}
	return strings.Join(nxt[:], "")
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
	cur := line
	for i := 0; i < 40; i++ {
		cur = step(cur)
	}
	fmt.Printf("1: %v, %v\n", len(cur), time.Since(t1))

	t2 := time.Now()
	cur = line
	for i := 0; i < 50; i++ {
		cur = step(cur)
	}
	fmt.Printf("2: %v, %v\n", len(cur), time.Since(t2))
}
