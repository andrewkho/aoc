package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
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
	var line string
	for scanner.Scan() {
		line = scanner.Text()
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))

	t1 := time.Now()

	var dfs func(i int, j int, recurse bool) int
	dfs = func(i int, k int, recurse bool) int {
		t := 0
		for i < k {
			if line[i] != '(' {
				t++
				i++
			} else {
				// i == '('
				j := i + 1
				for line[j] >= '0' && line[j] <= '9' {
					j++
				}
				var c, r int
				if c, err = strconv.Atoi(line[i+1 : j]); err != nil {
					log.Fatal(line[i+1 : j])
				}
				i = j // i == 'x'
				j = i + 1
				for line[j] >= '0' && line[j] <= '9' {
					j++
				}
				if r, err = strconv.Atoi(line[i+1 : j]); err != nil {
					log.Fatal(line[i+1 : j])
				}
				i = j + 1 // j == ')'
				j = i + c
				if recurse {
					t += r * dfs(i, j, recurse)
				} else {
					t += r * c
				}
				i = j
			}
		}
		return t
	}
	total := dfs(0, len(line), false)
	fmt.Printf("1: %v, %v\n", total, time.Since(t1))

	t2 := time.Now()
	total = dfs(0, len(line), true)
	fmt.Printf("2: %v, %v\n", total, time.Since(t2))
}
