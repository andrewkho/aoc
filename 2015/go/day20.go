package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strconv"
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
	scanner := bufio.NewScanner(file)

	var N int
	for scanner.Scan() {
		line := scanner.Text()
		if N, err = strconv.Atoi(line); err != nil {
			log.Fatal(line)
		}
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))
	fmt.Println(N)

	t1 := time.Now()
	// Sieve
	MAX := int(1e6)
	results := make([]int, MAX)
	minHouse := -1
outer:
	for i := 1; i < MAX; i++ {
		for j := i; j < MAX; j += i {
			results[j] += 10 * i
			if results[j] >= N {
				minHouse = j
				break outer
			}
		}
	}
	fmt.Printf("1: %v, %v\n", minHouse, time.Since(t1))

	t2 := time.Now()
	results = make([]int, MAX)
	minHouse = -1
outer2:
	for i := 1; i < MAX; i++ {
		for j := i; j < 51*i && j < MAX; j += i {
			results[j] += 11 * i
			if results[j] >= N {
				minHouse = j
				break outer2
			}
		}
	}
	fmt.Printf("2: %v, %v\n", minHouse, time.Since(t2))
}
