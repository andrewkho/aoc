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
	scanner := bufio.NewScanner(file)
	var lines []string
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))

	t1 := time.Now()
	total := 0
	for _, line := range lines {
		c := 0
		i := 1
		for i < len(line)-1 {
			switch line[i] {
			case '\\':
				if line[i+1] == '"' {
					i += 2
				} else if line[i+1] == 'x' {
					i += 4
				} else if line[i+1] == '\\' {
					i += 2
				}
			default:
				i++
			}
			c++
		}
		total += len(line) - c
	}
	fmt.Printf("1: %v, %v\n", total, time.Since(t1))

	t2 := time.Now()
	total = 0
	for _, line := range lines {
		c := 2
		for _, v := range line {
			switch v {
			case '\\':
				c += 2
			case '"':
				c += 2
			default:
				c++
			}
		}
		total += c - len(line)
	}
	fmt.Printf("2: %v, %v\n", total, time.Since(t2))
}
