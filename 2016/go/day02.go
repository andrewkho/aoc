package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"path/filepath"
	"time"
)

type Step struct {
	dir string
	n   int
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

	steps := []string{}
	scanner := bufio.NewScanner(file)
	// re := regexp.MustCompile(`^.*(R|L)(\w.*)$`)
	for scanner.Scan() {
		line := scanner.Text()
		steps = append(steps, line)
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))

	t1 := time.Now()
	pos := [2]int{1, 1}
	key := []int{}
	for _, step := range steps {
		for _, x := range step {
			switch x {
			case 'U':
				if pos[1] > 0 {
					pos[1]--
				}
			case 'D':
				if pos[1] < 2 {
					pos[1]++
				}
			case 'R':
				if pos[0] < 2 {
					pos[0]++
				}
			case 'L':
				if pos[0] > 0 {
					pos[0]--
				}
			}
		}
		key = append(key, pos[1]*3+pos[0]+1)
	}
	fmt.Printf("1: %v, %v\n", key, time.Since(t1))

	t2 := time.Now()
	pos = [2]int{2, 2}
	keypad := [5][5]string{
		{"X", "X", "1", "X", "X"},
		{"X", "2", "3", "4", "X"},
		{"5", "6", "7", "8", "9"},
		{"X", "A", "B", "C", "X"},
		{"X", "X", "D", "X", "X"},
	}
	key2 := []string{}
	for _, step := range steps {
		for _, x := range step {
			switch x {
			case 'U':
				if float64(pos[1]) > math.Abs(float64(pos[0]-2)) {
					pos[1]--
				}
			case 'D':
				if float64(pos[1]) < 4-math.Abs(float64(pos[0]-2)) {
					pos[1]++
				}
			case 'R':
				if float64(pos[0]) < 4-math.Abs(float64(pos[1]-2)) {
					pos[0]++
				}
			case 'L':
				if float64(pos[0]) > math.Abs(float64(pos[1]-2)) {
					pos[0]--
				}
			}
		}
		key2 = append(key2, keypad[pos[1]][pos[0]])
	}
	fmt.Printf("2: %v, %v\n", key2, time.Since(t2))
}
