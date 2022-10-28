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

type Instr struct {
	i string
	a int
	b int
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

	instrs := []Instr{}
	re := regexp.MustCompile(`^(rect|rotate row|rotate column).*?([0-9]+).*?([0-9]+)$`)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		groups := re.FindStringSubmatch(line)
		if groups == nil {
			log.Panicln(line)
		}
		i := Instr{i: groups[1]}
		if val, err := strconv.Atoi(groups[2]); err != nil {
			log.Fatal(err)
		} else {
			i.a = val
		}
		if val, err := strconv.Atoi(groups[3]); err != nil {
			log.Fatal(err)
		} else {
			i.b = val
		}
		instrs = append(instrs, i)
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))

	t1 := time.Now()
	grid := [6][50]int{}
	for _, instr := range instrs {
		switch instr.i {
		case "rect":
			for j := 0; j < instr.b; j++ {
				for i := 0; i < instr.a; i++ {
					grid[j][i] = 1
				}
			}
		case "rotate column":
			i := instr.a
			n := instr.b
			tmp := [6]int{}
			for j := 0; j < 6; j++ {
				lookup := (j - n) % 6
				if lookup < 0 {
					lookup += 6
				}
				tmp[j] = grid[lookup][i]
			}
			for j := 0; j < 6; j++ {
				grid[j][i] = tmp[j]
			}
		case "rotate row":
			j := instr.a
			n := instr.b
			tmp := [50]int{}
			for i := 0; i < 50; i++ {
				lookup := (i - n) % 50
				if lookup < 0 {
					lookup += 50
				}
				tmp[i] = grid[j][lookup]
			}
			grid[j] = tmp
		}
	}
	total := 0
	for j := 0; j < 6; j++ {
		for i := 0; i < 50; i++ {
			total += grid[j][i]
		}
	}
	fmt.Printf("1: %v, %v\n", total, time.Since(t1))

	t2 := time.Now()
	for j := 0; j < 6; j++ {
		line := [60]rune{}
		space := -1
		for i := 0; i < 50; i++ {
			if i%5 == 0 {
				space++
			}
			if grid[j][i] == 1 {
				line[i+space] = '#'
			} else {
				line[i+space] = ' '
			}
		}
		fmt.Println(string(line[:]))
	}
	fmt.Printf("2: %v, %v\n", total, time.Since(t2))
}
