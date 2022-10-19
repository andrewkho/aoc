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
	capacity := []int{}
	durability := []int{}
	flavor := []int{}
	texture := []int{}
	calories := []int{}

	re := regexp.MustCompile(`^(.*): capacity (-?[0-9].*), durability (-?[0-9].*), flavor (-?[0-9].*), texture (-?[0-9].*), calories (-?[0-9].*)`)
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
			capacity = append(capacity, val)
		}
		if val, err := strconv.Atoi(groups[3]); err != nil {
			log.Fatal(groups[3])
		} else {
			durability = append(durability, val)
		}
		if val, err := strconv.Atoi(groups[4]); err != nil {
			log.Fatal(groups[4])
		} else {
			flavor = append(flavor, val)
		}
		if val, err := strconv.Atoi(groups[5]); err != nil {
			log.Fatal(groups[5])
		} else {
			texture = append(texture, val)
		}
		if val, err := strconv.Atoi(groups[6]); err != nil {
			log.Fatal(groups[6])
		} else {
			calories = append(calories, val)
		}
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))

	N := len(names)
	C := 100

	t1 := time.Now()
	var score func(amounts []int) int
	score = func(amounts []int) int {
		sums := [5]int{} // 5 properties
		for i := 0; i < N; i++ {
			sums[0] += amounts[i] * capacity[i]
			sums[1] += amounts[i] * durability[i]
			sums[2] += amounts[i] * flavor[i]
			sums[3] += amounts[i] * texture[i]
			sums[4] += amounts[i] * calories[i]
		}

		prod := 1
		for j := 0; j < 4; j++ { // Ignore calories
			if sums[j] >= 0 {
				prod *= sums[j]
			} else {
				prod *= 0
			}
		}
		return prod
	}

	bst := 0
	useCals := false
	var dfs func(amounts []int, i int, remaining int, remainingCals int)
	dfs = func(amounts []int, i int, remaining int, remainingCals int) {
		if i == N-1 {
			amounts[i] = remaining
			remainingCals -= remaining * calories[i]
			if useCals && remainingCals != 0 {
				return
			}
			total := score(amounts)
			if total > bst {
				bst = total
			}
			amounts[i] = 0
			return
		}
		for j := 0; j <= remaining && remainingCals-j*calories[i] > 0; j++ {
			amounts[i] = j
			dfs(amounts, i+1, remaining-j, remainingCals-j*calories[i])
			amounts[i] = 0
		}
	}
	amounts := make([]int, N)
	dfs(amounts, 0, C, 1<<63-1)
	fmt.Printf("1: %v, %v\n", bst, time.Since(t1))

	t2 := time.Now()
	bst = 0
	useCals = true
	dfs(amounts, 0, C, 500)
	fmt.Printf("2: %v, %v\n", bst, time.Since(t2))
}
