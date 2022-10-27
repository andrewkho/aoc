package main

import (
	"bufio"
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

	codes := []string{}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		codes = append(codes, line)
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))

	t1 := time.Now()
	W := len(codes[0])
	counts := make([]map[rune]int, W)
	for w := 0; w < W; w++ {
		counts[w] = make(map[rune]int)
	}
	for _, code := range codes {
		for w, c := range code {
			counts[w][c]++
		}
	}
	message := make([]rune, W)
	for w, counter := range counts {
		bstCount := 0
		for k, v := range counter {
			if v > bstCount {
				bstCount = v
				message[w] = k
			}
		}
	}
	fmt.Printf("1: %v, %v\n", string(message), time.Since(t1))

	t2 := time.Now()
	message = make([]rune, W)
	for w, counter := range counts {
		bstCount := 1<<63 - 1
		for k, v := range counter {
			if v < bstCount {
				bstCount = v
				message[w] = k
			}
		}
	}
	fmt.Printf("2: %v, %v\n", string(message), time.Since(t2))
}
