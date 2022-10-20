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

type Stats struct {
	hp  int
	dmg int
	arm int
}

func play(player, boss Stats) bool {
	// All you need to know is number of attacks to kill
	playerDmg := player.dmg - boss.arm
	if playerDmg < 1 {
		playerDmg = 1
	}
	nPlayer := (boss.hp + (playerDmg - 1)) / playerDmg

	bossDmg := boss.dmg - player.arm
	if bossDmg < 1 {
		bossDmg = 1
	}
	nBoss := (player.hp + (bossDmg - 1)) / bossDmg

	return nPlayer <= nBoss
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

	var boss Stats
	re := regexp.MustCompile(`^(Hit Points|Damage|Armor): (\w.*)$`)
	for scanner.Scan() {
		line := scanner.Text()
		groups := re.FindStringSubmatch(line)
		if groups == nil {
			log.Panicln(line)
		}
		var val int
		if val, err = strconv.Atoi(groups[2]); err != nil {
			log.Fatal(groups[2])
		}
		switch groups[1] {
		case "Hit Points":
			boss.hp = val
		case "Damage":
			boss.dmg = val
		case "Armor":
			boss.arm = val
		}
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))
	fmt.Println(boss)

	t1 := time.Now()
	WEAPONS := []int{4, 5, 6, 7, 8}
	WEAPONSC := []int{8, 10, 25, 40, 74}
	ARMOR := []int{0, 1, 2, 3, 4, 5}
	ARMORC := []int{0, 13, 31, 53, 75, 102}
	RINGS := []int{0, 0, 1, 2, 3, -1, -2, -3}
	RINGSC := []int{0, 0, 25, 50, 100, 20, 40, 80}

	getBest := func(part int) int {
		sign := 1
		bst := 1<<63 - 1
		if part == 2 {
			sign = -1
		}
		for iw, w := range WEAPONS {
			for ia, a := range ARMOR {
				for ir1, r1 := range RINGS {
					for ir2 := ir1 + 1; ir2 < len(RINGS); ir2++ {
						r2 := RINGS[ir2]

						cost := WEAPONSC[iw] + ARMORC[ia] + RINGSC[ir1] + RINGSC[ir2]
						player := Stats{hp: 100, dmg: w, arm: a}
						if r1 < 0 {
							player.arm -= r1
						} else {
							player.dmg += r1
						}
						if r2 < 0 {
							player.arm -= r2
						} else {
							player.dmg += r2
						}
						if sign*cost < bst {
							if part == 1 && play(player, boss) {
								bst = sign * cost
							} else if part == 2 && !play(player, boss) {
								bst = sign * cost
							}
						}
					}
				}
			}
		}
		return sign * bst
	}
	fmt.Printf("1: %v, %v\n", getBest(1), time.Since(t1))

	t2 := time.Now()
	fmt.Printf("2: %v, %v\n", getBest(2), time.Since(t2))
}
