package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"regexp"
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

	N := 500
	facts := make([]map[string]int, N)
	for i := 0; i < N; i++ {
		facts[i] = make(map[string]int)
	}

	re := regexp.MustCompile(`^Sue ([0-9].*): (.*): ([0-9].*), (.*): ([0-9].*), (.*): ([0-9].*)$`)
	for scanner.Scan() {
		line := scanner.Text()
		groups := re.FindStringSubmatch(line)
		if groups == nil {
			log.Panicln(line)
		}
		var i int
		if i, err = strconv.Atoi(groups[1]); err != nil {
			log.Fatal(groups[1])
		}
		i--

		for j := 0; j < 3; j++ {
			if val, err := strconv.Atoi(groups[3+2*j]); err != nil {
				log.Fatal(groups[3+2*j])
			} else {
				facts[i][groups[2+2*j]] = val
			}
		}
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))

	t1 := time.Now()
	ticker := make(map[string]int)
	ticker["children"] = 3
	ticker["cats"] = 7
	ticker["samoyeds"] = 2
	ticker["pomeranians"] = 3
	ticker["akitas"] = 0
	ticker["vizslas"] = 0
	ticker["goldfish"] = 5
	ticker["trees"] = 3
	ticker["cars"] = 2
	ticker["perfumes"] = 1

	candidates := []int{}
outer:
	for i := 0; i < N; i++ {
		for k, v := range facts[i] {
			if ticker[k] != v {
				continue outer
			}
		}
		candidates = append(candidates, i+1)
	}
	fmt.Printf("1: %v, %v\n", candidates, time.Since(t1))

	t2 := time.Now()
	ops := make(map[string]string)
	ops["cats"] = ">"
	ops["trees"] = ">"
	ops["pomeranians"] = "<"
	ops["goldfish"] = "<"

	candidates = []int{}
outer2:
	for i := 0; i < N; i++ {
		for k, v := range facts[i] {
			switch ops[k] {
			case "":
				if ticker[k] != v {
					continue outer2
				}
			case ">":
				if v <= ticker[k] {
					continue outer2
				}
			case "<":
				if v >= ticker[k] {
					continue outer2
				}
			default:
				log.Fatal(ops[k], k)
			}
		}
		candidates = append(candidates, i+1)
	}
	fmt.Printf("2: %v, %v\n", candidates, time.Since(t2))
}
