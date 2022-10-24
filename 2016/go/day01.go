package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
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

	steps := []Step{}
	scanner := bufio.NewScanner(file)
	re := regexp.MustCompile(`^.*(R|L)(\w.*)$`)
	for scanner.Scan() {
		line := scanner.Text()
		for _, x := range strings.Split(line, ",") {
			groups := re.FindStringSubmatch(x)
			if groups == nil {
				log.Panicln(x)
			}
			if val, err := strconv.Atoi(groups[2]); err != nil {
				log.Fatal(groups[2])
			} else {
				steps = append(steps, Step{dir: groups[1], n: val})
			}
		}
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))
	fmt.Println(steps)

	t1 := time.Now()
	pos := [2]int{}
	face := 0
	for _, step := range steps {
		if step.dir == "R" {
			face = (face + 1) % 4
		} else {
			face = (face - 1) % 4
			if face < 0 {
				face += 4
			}
		}

		switch face {
		case 0: // N
			pos[0] += step.n
		case 1: // E
			pos[1] += step.n
		case 2: // S
			pos[0] -= step.n
		case 3: // W
			pos[1] -= step.n
		}
	}
	fmt.Printf("1: %v, %v, %v\n", pos, math.Abs(float64(pos[0]))+math.Abs(float64(pos[1])), time.Since(t1))

	t2 := time.Now()
	visited := make(map[[2]int]bool)
	pos = [2]int{}
	visited[pos] = true
	face = 0
outer:
	for _, step := range steps {
		if step.dir == "R" {
			face = (face + 1) % 4
		} else {
			face = (face - 1) % 4
			if face < 0 {
				face += 4
			}
		}

		for i := 0; i < step.n; i++ {
			switch face {
			case 0: // N
				pos[0]++
			case 1: // E
				pos[1]++
			case 2: // S
				pos[0]--
			case 3: // W
				pos[1]--
			}
			if visited[pos] {
				break outer
			}
			visited[pos] = true
		}
	}
	fmt.Printf("2: %v, %v, %v\n", pos, math.Abs(float64(pos[0]))+math.Abs(float64(pos[1])), time.Since(t2))
}
