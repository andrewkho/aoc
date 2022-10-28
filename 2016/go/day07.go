package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
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

	ips := []string{}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		ips = append(ips, line)
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))
	fmt.Println(len(ips))

	t1 := time.Now()
	total := 0
	for _, ip := range ips {
		bracket := 0
		isTLS := false
	inner:
		for j, c := range ip[:len(ip)-3] {
			switch c {
			case '[':
				bracket++
			case ']':
				bracket--
			default:
				if ip[j+3] == byte(c) && ip[j+1] != byte(c) && ip[j+1] == ip[j+2] {
					if bracket == 0 {
						isTLS = true
					} else {
						isTLS = false
						break inner
					}
				}
			}
		}
		if isTLS {
			total++
		}
	}
	fmt.Printf("1: %v, %v\n", total, time.Since(t1))

	t2 := time.Now()
	total = 0
outer:
	for _, ip := range ips {
		abas := make(map[string]bool)
		babs := make(map[string]bool)
		bracket := 0
		for j, c := range ip[:len(ip)-2] {
			switch c {
			case '[':
				bracket++
			case ']':
				bracket--
			default:
				if ip[j] != ip[j+1] && ip[j] == ip[j+2] {
					if bracket == 0 {
						abas[string(ip[j:j+3])] = true
					} else {
						babs[string(ip[j:j+3])] = true
					}
				}
			}
		}
		for k := range abas {
			if babs[string([]byte{k[1], k[0], k[1]})] {
				total++
				continue outer
			}
		}
	}
	fmt.Printf("2: %v, %v\n", total, time.Since(t2))
}
