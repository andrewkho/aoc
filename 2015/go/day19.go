package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
	"time"
	"unicode"
)

func molToArr(molecule string) []string {
	arr := []string{}
	for i := 0; i < len(molecule); {
		j := i + 1
		for j < len(molecule) && unicode.IsLower(rune(molecule[j])) {
			j++
		}
		arr = append(arr, molecule[i:j])
		i = j
	}
	return arr
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

	N := 500
	facts := make([]map[string]int, N)
	for i := 0; i < N; i++ {
		facts[i] = make(map[string]int)
	}

	re := regexp.MustCompile(`^(.*) => (.*)$`)
	mode := 0
	tr := make(map[string][]string)
	var molecule string
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			mode++
			continue
		}
		if mode == 0 {
			groups := re.FindStringSubmatch(line)
			if groups == nil {
				log.Panicln(line)
			}
			tr[groups[1]] = append(tr[groups[1]], groups[2])
		} else {
			molecule = line
		}
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))
	fmt.Println(molecule)

	t1 := time.Now()
	arr := molToArr(molecule)
	if len(strings.Join(arr, "")) != len(molecule) {
		log.Fatal(strings.Join(arr, ""), arr)
	}

	distincts := make(map[string]bool)
	fmt.Println("len arr", len(tr))
	for i := range arr {
		orig := arr[i]
		for _, next := range tr[orig] {
			arr[i] = next
			distincts[strings.Join(arr, "")] = true
		}
		arr[i] = orig
	}
	fmt.Println("len arr", len(tr))

	fmt.Printf("1: %v, %v\n", len(distincts), time.Since(t1))

	t2 := time.Now()
	total := len(arr) - 1
	for _, mol := range arr {
		if mol == "Y" {
			total -= 2
		} else if mol == "Ar" || mol == "Rn" {
			total--
		}
	}
	fmt.Printf("2: %v, %v\n", total, time.Since(t2))

	// Try a greedy approach for fun
	// Note that the ordering of combos is non-deterministic
	// and changes the time required to complete
	t3 := time.Now()
	reduc := make(map[string]string)
	combos := []string{}
	for k, vs := range tr {
		for _, v := range vs {
			reduc[v] = k
			combos = append(combos, v)
		}
	}
	// reverse order by length
	sort.SliceStable(combos, func(i, j int) bool {
		return len(combos[i]) > len(combos[j])
	})
	fmt.Println(combos)

	var dfs func(count int, cur string) int
	dfs = func(count int, cur string) int {
		if cur == "e" {
			return count
		}

		for _, c := range combos {
			// For this to work in general we'd need to try all different
			// positions of replacements, not just first.
			cand := strings.Replace(cur, c, reduc[c], 1)
			if cand != cur {
				result := dfs(count+1, cand)
				if result >= 0 {
					return result
				}
			}
		}

		return -1
	}
	bst := dfs(0, molecule)
	fmt.Printf("2b: %v, %v\n", bst, time.Since(t3))
}
