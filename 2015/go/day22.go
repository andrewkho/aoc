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
	hp    int
	dmg   int
	arm   int
	mana  int
	spent int
}

type Character struct {
	stats   Stats
	effects []Effect
}

type Effect interface {
	name() string
	tick() Effect
	do(stats *Stats)
	undo(stats *Stats)
	expired() bool
}

type Shield struct {
	timer  int
	length int
}

func (s Shield) name() string {
	return "Shield"
}
func (s Shield) tick() Effect {
	return Shield{timer: s.timer - 1, length: s.length}
}
func (s Shield) do(stats *Stats) {
	if s.timer == s.length {
		stats.arm += 7
	}
}
func (s Shield) undo(stats *Stats) {
	if s.timer == 0 {
		stats.arm -= 7
	}
}
func (s Shield) expired() bool {
	return s.timer == 0
}

type Poison struct {
	timer int
}

func (p Poison) name() string {
	return "Poison"
}
func (p Poison) tick() Effect {
	return Poison{timer: p.timer - 1}
}
func (p Poison) do(stats *Stats) {
	stats.hp -= 3
}
func (p Poison) undo(stats *Stats) {
}
func (p Poison) expired() bool {
	return p.timer == 0
}

type Recharge struct {
	timer int
}

func (p Recharge) name() string {
	return "Recharge"
}
func (p Recharge) tick() Effect {
	return Recharge{timer: p.timer - 1}
}
func (p Recharge) do(stats *Stats) {
	stats.mana += 101
}
func (p Recharge) undo(stats *Stats) {
}
func (p Recharge) expired() bool {
	return p.timer == 0
}

var SPELLS []string = []string{"Magic Missile", "Drain", "Shield", "Poison", "Recharge"}

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
	var dfs func(turn int, player, boss Character, bst int, penalty int) int
	dfs = func(turn int, player, boss Character, bst int, penalty int) int {
		if player.stats.spent >= bst {
			return 1<<63 - 1
		}
		if turn%2 == 0 {
			player.stats.hp -= penalty
		}
		// fmt.Println("turn", turn, "Player", player, "Boss", boss, "bst", bst)
		// apply effects
		neff := len(player.effects) + len(boss.effects)
		expired := 0
		for _, c := range []*Character{&player, &boss} {
			newEffects := []Effect{}
			for _, effect := range c.effects {
				effect.do(&c.stats)
				dup := effect.tick()
				// remove expired effects
				if dup.expired() {
					dup.undo(&c.stats)
					expired++
				} else {
					newEffects = append(newEffects, dup)
				}
			}
			c.effects = newEffects
		}
		if len(player.effects)+len(boss.effects) != neff-expired {
			log.Fatal(neff, expired, player.effects, boss.effects)
		}
		// Check stop condition
		if player.stats.hp <= 0 {
			return 1<<63 - 1
		} else if boss.stats.hp <= 0 {
			// log.Println("Player wins ", player.stats.spent)
			return player.stats.spent
		}

		// play turn
		if turn%2 == 0 {
			for _, spell := range SPELLS {
				// play spell
				switch spell {
				case "Magic Missile":
					cost := 53
					if player.stats.mana < cost {
						continue
					}
					player.stats.spent += cost
					player.stats.mana -= cost
					boss.stats.hp -= 4
				case "Drain":
					cost := 73
					if player.stats.mana < cost {
						continue
					}
					player.stats.spent += cost
					player.stats.mana -= cost
					boss.stats.hp -= 2
					player.stats.hp += 2
				case "Shield":
					cost := 113
					isActive := false
					for _, active := range player.effects {
						if active.name() == spell {
							isActive = true
							break
						}
					}
					if player.stats.mana < cost || isActive {
						continue
					}
					player.stats.spent += cost
					player.stats.mana -= cost
					player.effects = append(player.effects, Shield{timer: 6, length: 6})
				case "Poison":
					cost := 173
					isActive := false
					for _, active := range boss.effects {
						if active.name() == spell {
							isActive = true
							break
						}
					}
					if player.stats.mana < cost || isActive {
						continue
					}
					player.stats.spent += cost
					player.stats.mana -= cost
					boss.effects = append(boss.effects, Poison{timer: 6})
				case "Recharge":
					cost := 229
					isActive := false
					for _, active := range player.effects {
						if active.name() == spell {
							isActive = true
							break
						}
					}
					if player.stats.mana < cost || isActive {
						continue
					}
					player.stats.spent += cost
					player.stats.mana -= cost
					player.effects = append(player.effects, Recharge{timer: 5})
				default:
					log.Fatal(spell)
				}

				result := dfs(turn+1, player, boss, bst, penalty)

				if result < bst {
					bst = result
				}

				switch spell {
				case "Magic Missile":
					cost := 53
					player.stats.spent -= cost
					player.stats.mana += cost
					boss.stats.hp += 4
				case "Drain":
					cost := 73
					player.stats.spent -= cost
					player.stats.mana += cost
					boss.stats.hp += 2
					player.stats.hp -= 2
				case "Shield":
					cost := 113
					player.stats.spent -= cost
					player.stats.mana += cost
					player.effects = player.effects[:len(player.effects)-1]
				case "Poison":
					cost := 173
					player.stats.spent -= cost
					player.stats.mana += cost
					boss.effects = boss.effects[:len(boss.effects)-1]
				case "Recharge":
					cost := 229
					player.stats.spent -= cost
					player.stats.mana += cost
					player.effects = player.effects[:len(player.effects)-1]
				}
			}
			return bst
		} else {
			// boss turn
			dmg := boss.stats.dmg - player.stats.arm
			if dmg <= 0 {
				dmg = 1
			}

			player.stats.hp -= dmg
			return dfs(turn+1, player, boss, bst, penalty)
		}

	}
	playerStats := Stats{
		hp:   50,
		mana: 500,
	}
	bst := dfs(0, Character{stats: playerStats}, Character{stats: boss}, 1<<63-1, 0)
	fmt.Printf("1: %v, %v\n", bst, time.Since(t1))

	t2 := time.Now()
	bst = dfs(0, Character{stats: playerStats}, Character{stats: boss}, 1<<63-1, 1)
	fmt.Printf("2: %v, %v\n", bst, time.Since(t2))
}
