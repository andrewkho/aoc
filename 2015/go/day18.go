package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"time"
)

type Grid [102][102]int

func step(grid *Grid) *Grid {
	next := Grid{}

	for j := 1; j < 101; j++ {
		for i := 1; i < 101; i++ {
			nei := 0
			for dj := -1; dj <= 1; dj++ {
				for di := -1; di <= 1; di++ {
					nei += grid[j+dj][i+di]
				}
			}
			if grid[j][i] == 1 {
				// Adjust for including (j, i)
				nei--
				if nei == 2 || nei == 3 {
					next[j][i] = 1
				} // else off
			} else {
				if nei == 3 {
					next[j][i] = 1
				}
			}
		}
	}

	return &next
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
	scanner := bufio.NewScanner(file)

	grid := &Grid{} // Use extra space for boundary conditions
	for j := 0; scanner.Scan(); j++ {
		line := scanner.Text()
		for i, c := range line {
			if c == '#' {
				grid[j+1][i+1] = 1
			} // else 0
		}
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))

	t1 := time.Now()
	cur := &Grid{}
	*cur = *grid
	for i := 0; i < 100; i++ {
		cur = step(cur)
	}
	total := 0
	for _, row := range cur {
		for _, val := range row {
			total += val
		}
	}
	fmt.Printf("1: %v, %v\n", total, time.Since(t1))

	t2 := time.Now()
	*cur = *grid
	cur[1][1] = 1
	cur[1][100] = 1
	cur[100][1] = 1
	cur[100][100] = 1
	for i := 0; i < 100; i++ {
		cur = step(cur)
		cur[1][1] = 1
		cur[1][100] = 1
		cur[100][1] = 1
		cur[100][100] = 1
	}
	total = 0
	for _, row := range cur {
		for _, val := range row {
			total += val
		}
	}
	fmt.Printf("2: %v, %v\n", total, time.Since(t2))
}
