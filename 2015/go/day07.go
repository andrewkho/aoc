package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
	"time"
)

type Instruction struct {
	op    string
	left  string
	right string
}

func (inst *Instruction) eval(values map[string]uint16) uint16 {
	switch inst.op {
	case "NOP":
		return values[inst.right]
	case "NOT":
		return ^values[inst.right]
	case "AND":
		return values[inst.left] & values[inst.right]
	case "OR":
		return values[inst.left] | values[inst.right]
	case "RSHIFT":
		return values[inst.left] >> values[inst.right]
	case "LSHIFT":
		return values[inst.left] << values[inst.right]
	default:
		log.Fatal(inst)
	}
	log.Fatal(inst)
	return 0
}

var RE_BIN_OP *regexp.Regexp = regexp.MustCompile(`^(.*) (AND|OR|LSHIFT|RSHIFT) (.*)$`)
var RE_NOT *regexp.Regexp = regexp.MustCompile(`^(NOT) (.*)$`)

type Graph struct {
	values   map[string]uint16
	instr    map[string]*Instruction
	edges    map[string][]string
	indegree map[string]int
}

func (graph *Graph) addEdge(out string, in string) {
	graph.edges[out] = append(graph.edges[out], in)
	graph.indegree[in]++
}

func (graph *Graph) parseInstruction(x string, instr string) {
	graph.indegree[x] += 0 // ensure this node exists

	// parse out dependencies
	// Check if this is just a value
	if val, err := strconv.Atoi(instr); err == nil {
		graph.values[x] = uint16(val)
		return
	}
	// Check if binary operation
	groups := RE_BIN_OP.FindStringSubmatch(instr)
	if groups != nil {
		left := groups[1]
		op := groups[2]
		right := groups[3]
		graph.instr[x] = &Instruction{op: op, left: left, right: right}
		if val, err := strconv.Atoi(left); err != nil {
			graph.addEdge(left, x)
		} else {
			graph.values[left] = uint16(val)
		}
		if val, err := strconv.Atoi(right); err != nil {
			graph.addEdge(right, x)
		} else {
			graph.values[right] = uint16(val)
		}
		return
	}
	// check if NOT operation
	groups = RE_NOT.FindStringSubmatch(instr)
	if groups != nil {
		op := groups[1]
		right := groups[2]
		graph.addEdge(right, x)
		graph.instr[x] = &Instruction{op: op, right: right}
		return
	}
	// this must be just a wire
	graph.addEdge(instr, x)
	graph.instr[x] = &Instruction{op: "NOP", right: instr}
}

func (graph *Graph) eval() {
	q := []string{}
	for k, v := range graph.indegree {
		if v == 0 {
			q = append(q, k)
			delete(graph.indegree, k)
		}
	}

	for len(q) > 0 {
		node := q[0]
		q = q[1:]

		for _, x := range graph.edges[node] {
			graph.indegree[x]--
			if graph.indegree[x] == 0 {
				// we can process x
				q = append(q, x)
				delete(graph.indegree, x)

				graph.values[x] = graph.instr[x].eval(graph.values)
			}
		}
	}
}

func readGraph(filename string) *Graph {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)

	graph := &Graph{}
	graph.values = make(map[string]uint16)
	graph.instr = make(map[string]*Instruction)
	graph.edges = make(map[string][]string)
	graph.indegree = make(map[string]int)

	for scanner.Scan() {
		line := scanner.Text()
		splits := strings.Split(line, " -> ")

		x := splits[1]
		graph.parseInstruction(x, splits[0])
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return graph
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
	t1 := time.Now()
	fmt.Printf("Reading from %s,", filename)
	graph := readGraph(filename)
	fmt.Printf(" took %v\n", time.Since(t1))

	graph.eval()
	fmt.Printf("1: %v, %v\n", graph.values["a"], time.Since(t1))

	aval := graph.values["a"]

	t2 := time.Now()
	fmt.Printf("Reading from %s,", filename)
	graph = readGraph(filename)
	graph.values["b"] = aval
	fmt.Printf(" took %v\n", time.Since(t2))

	graph.eval()
	fmt.Printf("2: %v, %v\n", graph.values["a"], time.Since(t2))
}
