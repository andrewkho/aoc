package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"
)

type present struct {
	l int
	w int
	h int
}

func (p *present) smallest() (int, int, int) {
	s := p.l * p.w
	s1 := p.l
	s2 := p.w
	if p.w*p.h < s {
		s = p.w * p.h
		s1 = p.w
		s2 = p.h
	}
	if p.h*p.l < s {
		s = p.h * p.l
		s1 = p.h
		s2 = p.l
	}
	return s, s1, s2
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

	var dims []present
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		strs := strings.Split(scanner.Text(), `x`)
		if len(strs) != 3 {
			log.Fatal(scanner.Text())
		}
		var ints [3]int
		for i, s := range strs {
			if val, err := strconv.Atoi(s); err != nil {
				log.Fatal(err)
			} else {
				ints[i] = val
			}
		}
		dims = append(dims, present{l: ints[0], w: ints[1], h: ints[2]})
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))

	t1 := time.Now()
	total := 0
	for _, p := range dims {
		// fmt.Println("%v, %v", p, p.smallest())
		smallest, _, _ := p.smallest()
		total += 2*p.l*p.w + 2*p.w*p.h + 2*p.h*p.l + smallest
	}
	fmt.Printf("1: %v, %v\n", total, time.Since(t1))

	t2 := time.Now()
	total = 0
	for _, p := range dims {
		_, s1, s2 := p.smallest()
		total += 2*(s1+s2) + p.l*p.w*p.h
	}
	fmt.Printf("2: %v, %v\n", total, time.Since(t2))
}
