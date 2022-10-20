package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"sort"
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

	amounts := []int{}
	for scanner.Scan() {
		line := scanner.Text()
		if val, err := strconv.Atoi(line); err != nil {
			log.Fatal(line)
		} else {
			amounts = append(amounts, val)
		}
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))

	t1 := time.Now()
	N := len(amounts)
	T := 150
	sort.Ints(amounts)
	fmt.Println(amounts)
	var dfs func(i int, remaining int, count int) (int, int)
	dfs = func(i int, remaining int, count int) (int, int) {
		if remaining == 0 {
			return 1, count
		} else if remaining < 0 || i >= N {
			return 0, N + 1
		}
		total := 0
		least := N + 1
		c, l := dfs(i+1, remaining, count) // don't use this container
		total += c
		if l < least {
			least = l
		}
		c, l = dfs(i+1, remaining-amounts[i], count+1) // use this container
		total += c
		if l < least {
			least = l
		}

		return total, least
	}

	total, least := dfs(0, T, 0)
	fmt.Printf("1: %v, %v, %v\n", total, least, time.Since(t1))

	dfs = func(i int, remaining int, count int) (int, int) {
		if count == least && remaining == 0 {
			return 1, count
		} else if remaining < 0 || i >= N || count > least {
			return 0, N + 1
		}
		total := 0
		least := N + 1
		c, l := dfs(i+1, remaining, count) // don't use this container
		total += c
		if l < least {
			least = l
		}
		c, l = dfs(i+1, remaining-amounts[i], count+1) // use this container
		total += c
		if l < least {
			least = l
		}

		return total, least
	}

	t2 := time.Now()
	total, least = dfs(0, T, 0)
	fmt.Printf("2: %v, %v, %v\n", total, least, time.Since(t2))
}
