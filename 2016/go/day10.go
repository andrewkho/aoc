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

type Node struct {
	name  string
	chips []int
	low   *Node
	high  *Node
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

	rebot := regexp.MustCompile(`^bot ([0-9]+).*(output|bot) ([0-9]+) .* (output|bot) ([0-9]+)$`)
	reval := regexp.MustCompile(`^value ([0-9]+).* bot ([0-9]+)$`)
	scanner := bufio.NewScanner(file)
	bots := make(map[string]*Node)
	outputs := make(map[string]*Node)
	q := []*Node{}
	for scanner.Scan() {
		line := scanner.Text()
		groups := rebot.FindStringSubmatch(line)
		if groups != nil {
			var bot, low, high *Node
			var ok bool
			if groups[2] == "output" {
				if low, ok = outputs[groups[3]]; !ok {
					outputs[groups[3]] = &Node{name: groups[3], chips: []int{}, low: nil, high: nil}
					low = outputs[groups[3]]
				}
			} else {
				if low, ok = bots[groups[3]]; !ok {
					bots[groups[3]] = &Node{name: groups[3], chips: []int{}, low: nil, high: nil}
					low = bots[groups[3]]
				}
			}
			if groups[4] == "output" {
				if high, ok = outputs[groups[5]]; !ok {
					outputs[groups[5]] = &Node{name: groups[5], chips: []int{}, low: nil, high: nil}
					high = outputs[groups[5]]
				}
			} else {
				if high, ok = bots[groups[5]]; !ok {
					bots[groups[5]] = &Node{name: groups[5], chips: []int{}, low: nil, high: nil}
					high = bots[groups[5]]
				}
			}

			if bot, ok = bots[groups[1]]; !ok {
				bots[groups[1]] = &Node{name: groups[1], chips: []int{}, low: nil, high: nil}
				bot = bots[groups[1]]
			}
			bot.low = low
			bot.high = high
			continue
		}
		groups = reval.FindStringSubmatch(line)
		if groups != nil {
			var bot *Node
			var ok bool
			if bot, ok = bots[groups[2]]; !ok {
				bots[groups[2]] = &Node{name: groups[2], chips: []int{}, low: nil, high: nil}
				bot = bots[groups[2]]
			}
			if chip, err := strconv.Atoi(groups[1]); err != nil {
				log.Fatal(groups[1])
			} else {
				bot.chips = append(bot.chips, chip)
				if len(bot.chips) == 2 {
					q = append(q, bot)
				}
			}
			continue
		}
		log.Fatal(line)

	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))
	fmt.Printf("%g\n", q)

	t1 := time.Now()
	var answer string
	for len(q) > 0 {
		node := q[len(q)-1]
		q = q[:len(q)-1]

		var low, high int
		if node.chips[0] < node.chips[1] {
			low = node.chips[0]
			high = node.chips[1]
		} else {
			high = node.chips[0]
			low = node.chips[1]
		}
		node.low.chips = append(node.low.chips, low)
		node.high.chips = append(node.high.chips, high)
		if low == 17 && high == 61 {
			answer = node.name
			fmt.Println(answer)
		}
		node.chips = node.chips[:0]
		if len(node.low.chips) == 2 {
			q = append(q, node.low)
		}
		if len(node.high.chips) == 2 {
			q = append(q, node.high)
		}
	}
	fmt.Printf("1: %v, %v\n", answer, time.Since(t1))

	t2 := time.Now()
	total := 1
	for _, v := range "012" {
		total *= outputs[string(v)].chips[0]
	}
	fmt.Printf("2: %v, %v, %v, %v, %v\n", total, outputs["0"], outputs["1"], outputs["2"], time.Since(t2))
}
