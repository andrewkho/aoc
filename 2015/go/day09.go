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

type Edge struct {
	dest   string
	weight int
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

	graph := make(map[string][]Edge)

	re := regexp.MustCompile(`^(.*) to (.*) = (.*)$`)
	for scanner.Scan() {
		line := scanner.Text()
		groups := re.FindStringSubmatch(line)
		if groups == nil {
			log.Panicln(line)
		}
		left := groups[1]
		right := groups[2]
		if weight, err := strconv.Atoi(groups[3]); err != nil {
			log.Fatal(line)
		} else {
			graph[left] = append(graph[left], Edge{dest: right, weight: weight})
			graph[right] = append(graph[right], Edge{dest: left, weight: weight})
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))

	t1 := time.Now()
	// Add a dummy root node with zero distance
	for k, _ := range graph {
		graph["root"] = append(graph["root"], Edge{dest: k, weight: 0})
	}

	visited := make(map[string]bool)
	total := 0
	bst := 1<<63 - 1
	remaining := len(graph) - 1
	var dfs func(node string)
	dfs = func(node string) {
		if remaining == 0 {
			if total < bst {
				bst = total
			}
		}

		for _, edge := range graph[node] {
			if !visited[edge.dest] {
				visited[edge.dest] = true
				total += edge.weight
				remaining -= 1
				dfs(edge.dest)
				remaining += 1
				total -= edge.weight
				visited[edge.dest] = false
			}
		}
	}

	dfs("root")
	fmt.Printf("1: %v, %v\n", bst, time.Since(t1))

	t2 := time.Now()
	// To find max, let's just negate the weights
	for _, edges := range graph {
		for i, _ := range edges {
			edges[i].weight *= -1
		}
	}
	// because of backtracking, total and visited should be reset
	bst = 0
	dfs("root")
	fmt.Printf("2: %v, %v\n", -bst, time.Since(t2))
}
