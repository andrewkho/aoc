package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"time"
    "path/filepath"
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
	floor := 0
    for _, c := range line {
        switch c {
        case '(': floor += 1
        case ')': floor -= 1
        default: log.Fatal(c)
        }
    }
	fmt.Printf("1: %v, %v\n", floor, time.Since(t1))

	t2 := time.Now()
    floor = 0
    pos := -1
    for i, c := range line {
        switch c {
        case '(': floor += 1
        case ')': floor -= 1
        default: log.Fatal(c)
        }
        if floor < 0 {
            pos = i
            break
        }
    }
	fmt.Printf("2: %v, %v\n", pos+1, time.Since(t2))
}
