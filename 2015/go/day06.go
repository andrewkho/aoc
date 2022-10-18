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

type Limits [2][2]int
type Instruction struct {
	flip   string
	limits Limits
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
	var instructions []Instruction
	re := regexp.MustCompile(
		`^(turn on|turn off|toggle) ([0-9].*),([0-9].*) through ([0-9].*),([0-9].*)$`)
	for scanner.Scan() {
		line := scanner.Text()
		groups := re.FindStringSubmatch(line)
		if groups == nil {
			log.Panicln(line)
		}
		instr := Instruction{flip: groups[1]}
		for i := 0; i < 2; i++ {
			for dim := 0; dim < 2; dim++ {
				if val, err := strconv.Atoi(groups[2+2*i+dim]); err != nil {
					log.Panicln(err)
				} else {
					instr.limits[dim][i] = val
				}
			}
		}
		instructions = append(instructions, instr)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))

	t1 := time.Now()
	grid := [1000][1000]int{}
	for _, instr := range instructions {
		for j := instr.limits[1][0]; j < instr.limits[1][1]+1; j++ {
			for i := instr.limits[0][0]; i < instr.limits[0][1]+1; i++ {
				switch instr.flip {
				case "turn on":
					grid[j][i] = 1
				case "turn off":
					grid[j][i] = 0
				case "toggle":
					grid[j][i] = 1 - grid[j][i]
				default:
					log.Fatal(instr)
				}
			}
		}
	}
	total := 0
	for j := 0; j < 1000; j++ {
		for i := 0; i < 1000; i++ {
			total += grid[j][i]
		}
	}
	fmt.Printf("1: %v, %v\n", total, time.Since(t1))

	t2 := time.Now()
	grid = [1000][1000]int{}
	for _, instr := range instructions {
		for j := instr.limits[1][0]; j < instr.limits[1][1]+1; j++ {
			for i := instr.limits[0][0]; i < instr.limits[0][1]+1; i++ {
				switch instr.flip {
				case "turn on":
					grid[j][i] += 1
				case "turn off":
					if grid[j][i] > 0 {
						grid[j][i] -= 1
					}
				case "toggle":
					grid[j][i] += 2
				default:
					log.Fatal(instr)
				}
			}
		}
	}
	total = 0
	for j := 0; j < 1000; j++ {
		for i := 0; i < 1000; i++ {
			total += grid[j][i]
		}
	}
	fmt.Printf("2: %v, %v\n", total, time.Since(t2))
}
