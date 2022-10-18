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

	var strs []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		strs = append(strs, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))

	t1 := time.Now()

	VOWELS := make(map[rune]bool)
	for _, c := range "aeiou" {
		VOWELS[c] = true
	}

	DENY := make(map[string]bool)
	for _, c := range []string{"ab", "cd", "pq", "xy"} {
		DENY[c] = true
	}

	total := 0
outer:
	for _, s := range strs {
		vowels := 0
		doubles := 0
		if _, prs := VOWELS[rune(s[0])]; prs {
			vowels++
		}

		for i := 1; i < len(s); i++ {
			if _, prs := VOWELS[rune(s[i])]; prs {
				vowels++
			}
			if s[i] == s[i-1] {
				doubles++
			}
			if _, prs := DENY[s[i-1:i+1]]; prs {
				continue outer
			}
		}
		if vowels >= 3 && doubles > 0 {
			total++
		}
	}
	fmt.Printf("1: %v, %v\n", total, time.Since(t1))

	t2 := time.Now()
	type PairInfo struct {
		last  int
		count int
	}
	total = 0
	for _, s := range strs {
		pairs := make(map[string]*PairInfo)
		repeats := 0
		hasPair := false

		for i := 1; i < len(s); i++ {
			pair := s[i-1 : i+1]
			if entry, prs := pairs[pair]; !prs {
				pairs[pair] = &PairInfo{i - 1, 1}
			} else {
				if entry.last < i-2 {
					entry.last = i - 1
					entry.count++
					hasPair = true
				}
			}
			if i > 1 && s[i] == s[i-2] {
				repeats++
			}
		}
		if repeats > 0 && hasPair {
			total++
		}
	}

	fmt.Printf("2: %v, %v\n", total, time.Since(t2))
}
