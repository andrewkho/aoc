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
	"strings"
	"time"
)

type Room struct {
	name   string
	sector int
	cksum  string
}

func (r *Room) decrypt() string {
	dname := make([]rune, len(r.name))
	for i, c := range r.name {
		if c == '-' {
			dname[i] = ' '
		} else {
			dname[i] = rune((int(c)-int('a')+r.sector)%26 + int('a'))
		}
	}
	return string(dname)
}

type RuneCount struct {
	c     rune
	count int
}
type RuneCountSlice []RuneCount

func (d RuneCountSlice) Len() int {
	return len(d)
}

func (d RuneCountSlice) Swap(i, j int) {
	d[i], d[j] = d[j], d[i]
}

func (d RuneCountSlice) Less(i, j int) bool {
	if d[i].count == d[j].count {
		return d[i].c < d[j].c
	} else {
		return d[i].count >= d[j].count
	}
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

	rooms := []Room{}
	scanner := bufio.NewScanner(file)
	re := regexp.MustCompile(`^(.*?)([0-9]+)\[(.*?)\]$`)
	for scanner.Scan() {
		line := scanner.Text()
		groups := re.FindStringSubmatch(line)
		if groups == nil {
			log.Panicln(line)
		}
		if val, err := strconv.Atoi(groups[2]); err != nil {
			log.Fatal(groups[2], err)
		} else {
			rooms = append(rooms, Room{cksum: groups[3], sector: val, name: groups[1]})
		}
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))

	t1 := time.Now()
	total := 0
	for _, room := range rooms {
		counts := make(map[rune]int)
		for _, c := range room.name {
			if c == '-' {
				continue
			}
			counts[c]++
		}
		rc := make([]RuneCount, len(counts))
		i := 0
		for k, v := range counts {
			rc[i] = RuneCount{c: k, count: v}
			i++
		}
		sort.Sort(RuneCountSlice(rc))
		good := true
		for i, c := range rc[:5] {
			if c.c != rune(room.cksum[i]) {
				good = false
				break
			}
		}
		if good {
			total += room.sector
		}
	}
	fmt.Printf("1: %v, %v\n", total, time.Since(t1))

	t2 := time.Now()
	for _, room := range rooms {
		if strings.Contains(room.decrypt(), "north") {
			fmt.Println(room.decrypt(), room.sector)
			total = room.sector
		}
	}
	fmt.Printf("2: %v, %v\n", total, time.Since(t2))
}
