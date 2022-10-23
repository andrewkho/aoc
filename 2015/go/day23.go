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

type Instr struct {
	i string
	r int
	o int
}

func execute(program []Instr, registers [2]int) [2]int {
	pc := 0
	for pc < len(program) {
		i := program[pc]
		next := pc + 1
		switch i.i {
		case "inc":
			registers[i.r]++
		case "hlf":
			registers[i.r] /= 2
		case "tpl":
			registers[i.r] *= 3
		case "jmp":
			next = pc + i.o
		case "jie":
			if registers[i.r]%2 == 0 {
				next = pc + i.o
			}
		case "jio":
			if registers[i.r] == 1 {
				next = pc + i.o
			}
		default:
			log.Fatal(i)
		}
		pc = next
	}
	return registers
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

	instrs := []Instr{}
	re := regexp.MustCompile(`^(\w+?) ([\+|-]?\w+)(,?) ?(.*?)$`)
	for scanner.Scan() {
		line := scanner.Text()
		groups := re.FindStringSubmatch(line)
		if groups == nil {
			log.Panicln(line)
		}
		i := Instr{i: groups[1]}
		if groups[1] == "jmp" {
			if i.o, err = strconv.Atoi(groups[2]); err != nil {
				log.Fatal(err, line, groups)
			}
		} else {
			if groups[2] == "a" {
				i.r = 0
			} else if groups[2] == "b" {
				i.r = 1
			} else {
				log.Fatal(line, groups)
			}
		}
		if groups[1] == "jio" || groups[1] == "jie" {
			if i.o, err = strconv.Atoi(groups[4]); err != nil {
				log.Fatal(line, groups)
			}
		}
		fmt.Println(line, i)
		instrs = append(instrs, i)
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))
	fmt.Println("Instructions:", instrs)

	t1 := time.Now()
	registers := execute(instrs, [2]int{})
	fmt.Printf("1: %v, %v\n", registers, time.Since(t1))

	t2 := time.Now()
	registers = execute(instrs, [2]int{1, 0})
	fmt.Printf("2: %v, %v\n", registers, time.Since(t2))
}
