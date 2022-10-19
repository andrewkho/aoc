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

	type pair struct {
		a int
		b int
	}

	names := make(map[string]int)
	values := make(map[pair]int)

	re := regexp.MustCompile(`^(.*) would (gain|lose) ([0-9].*) happiness units by sitting next to (.*).$`)
	for scanner.Scan() {
		line := scanner.Text()
		groups := re.FindStringSubmatch(line)
		if groups == nil {
			log.Panicln(line)
		}
		name := groups[1]
		sign := 1
		if groups[2] == "lose" {
			sign = -1
		}
		var value int
		if val, err := strconv.Atoi(groups[3]); err != nil {
			log.Panicln(line)
		} else {
			value = sign * val
		}
		other := groups[4]

		if _, prs := names[name]; !prs {
			names[name] = len(names)
		}
		if _, prs := names[other]; !prs {
			names[other] = len(names)
		}
		values[pair{a: names[name], b: names[other]}] = value
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	N := len(names)
	m := make([][]int, N)
	for i := 0; i < N; i++ {
		m[i] = make([]int, N)
		for j := 0; j < N; j++ {
			m[i][j] = values[pair{a: i, b: j}]
		}
	}

	fmt.Printf(" took %v\n", time.Since(t0))

	t1 := time.Now()
	// Exhaustive search with backtracking
	visited := make([]bool, N)
	remaining := N
	var dfs func(node int)
	bst := -(1<<63 - 1)
	total := 0
	dfs = func(node int) {
		visited[node] = true
		remaining--
		if remaining == 0 {
			// We need to account for wrapping around
			total += m[node][0] + m[0][node]
			if total > bst {
				bst = total
			}
			total -= m[node][0] + m[0][node]
		}

		for i := 0; i < N; i++ {
			if visited[i] {
				continue
			}
			total += m[node][i] + m[i][node]
			dfs(i)
			total -= m[node][i] + m[i][node]
		}
		visited[node] = false
		remaining++
	}

	dfs(0)
	fmt.Printf("1: %v, %v\n", bst, time.Since(t1))

	t2 := time.Now()
	for i := 0; i < N; i++ {
		m[i] = append(m[i], 0)
	}
	N++
	remaining = N
	m = append(m, make([]int, N))
	visited = append(visited, false)
	bst = -(1<<63 - 1)
	total = 0
	dfs(0)
	fmt.Printf("2: %v, %v\n", bst, time.Since(t2))
}
