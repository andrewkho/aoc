package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"time"
)

type Coord struct {
	x int
	y int
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
	visits := make(map[Coord]int)
	pos := Coord{x: 0, y: 0}
	visits[pos] = 1
	for _, c := range line {
		switch c {
		case '^':
			pos.y += 1
		case '>':
			pos.x += 1
		case 'v':
			pos.y -= 1
		case '<':
			pos.x -= 1
		default:
			log.Fatal(c)
		}
		visits[pos] += 1
	}
	fmt.Printf("1: %v, %v\n", len(visits), time.Since(t1))

	t2 := time.Now()
	visits = make(map[Coord]int)
	var posarr [2]Coord
	visits[posarr[0]] = 2
	for i, c := range line {
		switch c {
		case '^':
			posarr[i%2].y += 1
		case '>':
			posarr[i%2].x += 1
		case 'v':
			posarr[i%2].y -= 1
		case '<':
			posarr[i%2].x -= 1
		default:
			log.Fatal(c)
		}
		visits[posarr[i%2]] += 1
	}
	fmt.Printf("2: %v, %v\n", len(visits), time.Since(t2))
}
