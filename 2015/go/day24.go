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

func canSplit(i int, groups []int, weights []int, used []bool, target int) bool {
	if i < 0 { // Check terminal condition
		v := groups[0]
		for _, v2 := range groups[1:] {
			if v != v2 {
				return false
			}
		}
		return true
	}
	if used[i] { // weight is used in center
		return canSplit(i-1, groups, weights, used, target)
	}

	for j := range groups {
		if groups[j]+weights[i] > target { // Prune if more than target weight
			continue
		}
		groups[j] += weights[i]
		if canSplit(i-1, groups, weights, used, target) {
			return true
		}
		groups[j] -= weights[i] // backtrack
	}
	return false
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

	weights := []int{}
	for scanner.Scan() {
		line := scanner.Text()
		if val, err := strconv.Atoi(line); err == nil {
			weights = append(weights, val)
		} else {
			log.Fatal(line)
		}
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))
	fmt.Println("Weights:", weights)

	t1 := time.Now()
	N := len(weights)
	bst := 1<<63 - 1
	bstCount := 1<<63 - 1
	var dfs func(i int, qe int, count int, remaining int, g1 int, weights []int, seen []bool, nGroups int, target int)
	dfs = func(i int, qe int, count int, remaining int, g1 int, weights []int, seen []bool, nGroups int, target int) {
		if count > bstCount || g1 > target {
			return
		}
		// Check terminal condition
		if g1 == target && canSplit(N-1, make([]int, nGroups), weights, seen, target) {
			if count < bstCount || (count == bstCount && qe < bst) {
				bst = qe
				bstCount = count
				return
			}
		}
		if i < 0 {
			return
		}

		// Try with and witout weight[i]
		dfs(i-1, qe, count, remaining, g1, weights, seen, nGroups, target)
		seen[i] = true
		dfs(i-1, qe*weights[i], count+1, remaining-weights[i], g1+weights[i], weights, seen, nGroups, target)
		seen[i] = false
	}
	remaining := 0
	for _, val := range weights {
		remaining += val
	}
	dfs(N-1, 1, 0, remaining, 0, weights, make([]bool, N), 2, remaining/3)
	fmt.Printf("1: %v, %v, %v\n", bst, bstCount, time.Since(t1))

	t2 := time.Now()
	bst = 1<<63 - 1
	bstCount = 1<<63 - 1
	dfs(N-1, 1, 0, remaining, 0, weights, make([]bool, N), 3, remaining/4)
	fmt.Printf("2: %v, %v, %v\n", bst, bstCount, time.Since(t2))
}
