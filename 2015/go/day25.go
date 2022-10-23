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

	var row, col int
	re := regexp.MustCompile(`^.*? row (\w.*), column (\w.*).$`)
	for scanner.Scan() {
		line := scanner.Text()
		groups := re.FindStringSubmatch(line)
		if groups == nil {
			log.Panicln(line)
		}
		if row, err = strconv.Atoi(groups[1]); err != nil {
			log.Fatal(groups[1])
		}
		if col, err = strconv.Atoi(groups[2]); err != nil {
			log.Fatal(groups[2])
		}
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))
	fmt.Println("row, col", row, col)

	t1 := time.Now()
	N := (row+col-2)*(row+col-1)/2 + col
	v := 20151125
	x := 252533
	y := 33554393
	for i := 1; i < N; i++ {
		v = (v * x) % y
	}
	fmt.Printf("1: %v, %v\n", v, time.Since(t1))

	t2 := time.Now()
	fmt.Printf("2: %v, %v\n", 22, time.Since(t2))
}
