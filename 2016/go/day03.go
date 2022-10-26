package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strconv"
	"time"
)

type Triangle [3]int

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

	tris := []Triangle{}
	scanner := bufio.NewScanner(file)
	re := regexp.MustCompile(`(\w+)\s+(\w+)\s+(\w+)`)
	for scanner.Scan() {
		line := scanner.Text()
		groups := re.FindStringSubmatch(line)
		if groups == nil {
			log.Panicln(line)
		}
		tri := Triangle{}
		for i := 0; i < 3; i++ {
			if val, err := strconv.Atoi(groups[i+1]); err != nil {
				log.Fatal(groups[i+1], err)
			} else {
				tri[i] = val
			}
		}
		tris = append(tris, tri)
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))

	t1 := time.Now()
	total := 0
	for _, tri := range tris {
		sort.Ints(tri[:])
		if tri[0]+tri[1] > tri[2] {
			total++
		}
	}
	fmt.Printf("1: %v, %v\n", total, time.Since(t1))

	t2 := time.Now()
	total = 0
	for i := 0; i < len(tris); i += 3 {
		newtris := [3]Triangle{}
		for di := 0; di < 3; di++ {
			for col := 0; col < 3; col++ {
				newtris[col][di] = tris[i+di][col]
			}
		}
		for _, tri := range newtris {
			sort.Ints(tri[:])
			if tri[0]+tri[1] > tri[2] {
				total++
			}
		}
	}
	fmt.Printf("2: %v, %v\n", total, time.Since(t2))
}
