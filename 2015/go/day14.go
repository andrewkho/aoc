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

	names := []string{}
	speed := []int{}
	duration := []int{}
	rest := []int{}

	re := regexp.MustCompile(`^(.*) can fly ([0-9].*) km/s for ([0-9].*) seconds, (.*) ([0-9].*) seconds.$`)
	for scanner.Scan() {
		line := scanner.Text()
		groups := re.FindStringSubmatch(line)
		if groups == nil {
			log.Panicln(line)
		}
		names = append(names, groups[1])
		if val, err := strconv.Atoi(groups[2]); err != nil {
			log.Fatal(groups[2])
		} else {
			speed = append(speed, val)
		}
		if val, err := strconv.Atoi(groups[3]); err != nil {
			log.Fatal(groups[3])
		} else {
			duration = append(duration, val)
		}
		if val, err := strconv.Atoi(groups[5]); err != nil {
			log.Fatal(groups[5])
		} else {
			rest = append(rest, val)
		}
	}
	N := len(names)
	T := 2503

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	fmt.Printf(" took %v\n", time.Since(t0))

	t1 := time.Now()
	bst := 0
	for i := 0; i < N; i++ {
		t := 0
		dist := 0
		for t < T {
			dt := duration[i]
			if T-t < dt {
				dt = T - t
			}
			dist += speed[i] * dt
			t += duration[i] + rest[i]
		}
		if dist > bst {
			bst = dist
		}
	}

	fmt.Printf("1: %v, %v\n", bst, time.Since(t1))

	t2 := time.Now()
	pos := make([]int, N)
	points := make([]int, N)
	for t := 0; t <= T; t++ {
		furthest := 0
		for i := 0; i < N; i++ {
			period := duration[i] + rest[i]
			if t%period < duration[i] {
				pos[i] += speed[i]
			}
			if pos[i] > furthest {
				furthest = pos[i]
			}
		}

		for i := 0; i < N; i++ {
			if pos[i] == furthest {
				points[i]++
			}
		}
	}
	bst = 0
	for i := 0; i < N; i++ {
		if points[i] > bst {
			bst = points[i]
		}
	}
	fmt.Printf("2: %v, %v\n", bst, time.Since(t2))
}
