package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"time"
)

type State struct {
	chipPos [7]int
	genPos  [7]int
	floor   int
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

	re := regexp.MustCompile(`((\w+)( generator|-compatible microchip))+`)
	scanner := bufio.NewScanner(file)

	index := make(map[string]int)

	state := &State{}
	floor := 0
	for scanner.Scan() {
		line := scanner.Text()
		matches := re.FindAllStringSubmatch(line, -1)
		for _, groups := range matches {
			var idx int
			var ok bool
			if idx, ok = index[groups[2]]; !ok {
				idx = len(index)
				index[groups[2]] = idx
			}
			if groups[3] == " generator" {
				state.genPos[idx] = floor
			} else {
				state.chipPos[idx] = floor
			}
		}
		floor++
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))
	fmt.Printf("%v\n", state)

	t1 := time.Now()
	// Do a BFS with memo
	bst := bfs(*state, 5)
	fmt.Printf("1: %v, %v\n", bst, time.Since(t1))

	t2 := time.Now()
	// the new element should already be zero-initialized
	fmt.Printf("%v\n", state)
	bst = bfs(*state, 7)
	fmt.Printf("2: %v, %v\n", bst, time.Since(t2))
}

type Pair struct {
	a int
	b int
}

// Take advantage of the fact that names of chips and generators
// don't affect number of steps to move them, only where they
// are located relative to each other
type Memo struct {
	positions [7]Pair
	floor     int
}

func getMemo(state *State, N int) Memo {
	memo := Memo{floor: state.floor}
	for i := 0; i < N; i++ {
		memo.positions[i].a = state.genPos[i]
		memo.positions[i].b = state.chipPos[i]
	}
	sort.Slice(memo.positions[:N], func(i, j int) bool {
		if memo.positions[i].a != memo.positions[j].a {
			return memo.positions[i].a < memo.positions[j].a
		} else {
			return memo.positions[i].b < memo.positions[j].b
		}
	})
	return memo
}

func bfs(start State, N int) int {
	state := &start
	seen := make(map[Memo]bool)
	seen[getMemo(state, N)] = true

	type Entry struct {
		state *State
		steps int
	}
	q := []*Entry{&Entry{state: state, steps: 0}}
	bst := 1<<63 - 1
	for len(q) > 0 {
		state = q[0].state
		steps := q[0].steps
		q = q[1:]

		if checkWin(state, N) {
			bst = steps
			break
		}
		for _, dfloor := range [2]int{1, -1} {
			if state.floor+dfloor < 0 || state.floor+dfloor >= 4 {
				continue
			}
			for idx1 := 0; idx1 < N*2; idx1++ {
				for idx2 := idx1; idx2 < N*2; idx2++ {
					pos1 := getPos(idx1, state, N)
					pos2 := getPos(idx2, state, N)

					if pos1 == state.floor && pos2 == state.floor {
						state2 := genState(state, dfloor, idx1, idx2, N)
						memo2 := getMemo(&state2, N)
						if !seen[memo2] && isValid(&state2, N) {
							seen[memo2] = true
							q = append(q, &Entry{state: &state2, steps: steps + 1})
						}
					}
				}
			}
		}
	}

	return bst
}

func isValid(state *State, N int) bool {
	for i := 0; i < N; i++ {
		if state.chipPos[i] == state.genPos[i] {
			continue
		}
		// Check if any other generator is on same floor as chip
		for j := 0; j < N; j++ {
			if i == j {
				continue
			}
			if state.chipPos[i] == state.genPos[j] {
				return false
			}
		}
	}
	return true
}

func checkWin(state *State, N int) (done bool) {
	for i := 0; i < N; i++ {
		if state.chipPos[i] != 3 || state.genPos[i] != 3 {
			return false
		}
	}
	return true
}

func getPos(tenIdx int, state *State, N int) int {
	if tenIdx/N == 0 {
		return state.chipPos[tenIdx]
	} else {
		return state.genPos[tenIdx%N]
	}
}

func genState(oldState *State, dfloor int, idx1 int, idx2 int, N int) State {
	state := State{
		floor:   oldState.floor + dfloor,
		chipPos: oldState.chipPos,
		genPos:  oldState.genPos,
	}

	if idx1/N == 0 {
		state.chipPos[idx1] += dfloor
	} else {
		state.genPos[idx1%N] += dfloor
	}

	if idx2 != idx1 {
		if idx2/N == 0 {
			state.chipPos[idx2] += dfloor
		} else {
			state.genPos[idx2%N] += dfloor
		}
	}

	return state
}
