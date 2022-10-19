package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"
	"time"
)

func initChrs() map[rune]int {
	chrs := make(map[rune]int)
	for i, c := range "abcdefghijklmnopqrstuvwxyz" {
		chrs[c] = i
	}
	return chrs
}

var CHRS map[rune]int = initChrs()
var ALPHA string = "abcdefghijklmnopqrstuvwxyz"

func step(cur *[8]int) {
	i := 7
	cur[i]++
	for i >= 0 && cur[i] == 26 {
		cur[i] = 0
		cur[i-1]++
		i--
	}
}

func check(cur *[8]int) bool {
	doubles := []int{}
	straight := false
	disallow := true

	for i := 0; i < 8; i++ {
		if cur[i] == CHRS['i'] || cur[i] == CHRS['o'] || cur[i] == CHRS['l'] {
			disallow = false
			break
		}
		if i >= 2 && !straight {
			if cur[i-2] == cur[i-1]-1 && cur[i-1] == cur[i]-1 {
				straight = true
			}
		}
		if i >= 1 && len(doubles) < 2 {
			if cur[i-1] == cur[i] {
				if len(doubles) > 0 && doubles[0] == cur[i] {
					continue
				}
				doubles = append(doubles, cur[i])
			}
		}
	}

	return len(doubles) == 2 && straight && disallow
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
	fmt.Println(line)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	fmt.Printf(" took %v\n", time.Since(t0))
	t1 := time.Now()
	cur := &[8]int{}
	for i, c := range line {
		cur[i] = CHRS[c]
	}
	for !check(cur) {
		step(cur)
	}
	result := [8]string{}
	for i, v := range cur {
		result[i] = string(ALPHA[v])
	}
	fmt.Printf("1: %v, %v\n", strings.Join(result[:], ""), time.Since(t1))

	step(cur)
	for !check(cur) {
		step(cur)
	}
	for i, v := range cur {
		result[i] = string(ALPHA[v])
	}
	t2 := time.Now()
	fmt.Printf("2: %v, %v\n", strings.Join(result[:], ""), time.Since(t2))
}
