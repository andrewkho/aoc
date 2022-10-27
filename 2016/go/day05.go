package main

import (
	"bufio"
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"time"
)

type HashGenerator struct {
	nprefix int
	i       int
	width   int
	text    []byte
}

func NewHashGenerator(prefix string) HashGenerator {
	hg := HashGenerator{
		nprefix: len(prefix),
		i:       0,
		width:   1,
		text:    make([]byte, len(prefix)+10),
	}
	for i, c := range prefix {
		hg.text[i] = byte(c)
	}

	return hg
}

func (h *HashGenerator) next() [16]byte {
	h.i++
	rem := h.i
	for w := h.width - 1; w >= 0; w-- {
		h.text[h.nprefix+w] = byte('0') + byte(rem%10)
		rem /= 10
	}
	if rem != 0 {
		// This should happen very rarely, O(log(n))
		h.width++
		rem = h.i
		for w := h.width - 1; w >= 0; w-- {
			h.text[h.nprefix+w] = byte('0') + byte(rem%10)
			rem /= 10
		}
	}
	return md5.Sum(h.text[:h.nprefix+h.width])
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
	var prefix string
	for scanner.Scan() {
		line := scanner.Text()
		prefix = line
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))
	fmt.Println(prefix)

	t1 := time.Now()
	password := [8]rune{}
	hits := 0
	mask := byte(15 << 4)
	hg := NewHashGenerator(prefix)
	for hits < 8 {
		hash := hg.next()
		// Looking for 5 zeros, each zero is 4 bits, we need 20 bits = 2.5 bytes
		if hash[0] == 0 && hash[1] == 0 && hash[2]&mask == 0 {
			x := hex.EncodeToString(hash[:])
			password[hits] = rune(x[5])
			hits++
			fmt.Printf("decrypting... %v %v %v\n", hg.i, x, password)
		}
	}
	fmt.Printf("1: %v, %v\n", string(password[:]), time.Since(t1))

	t2 := time.Now()
	password = [8]rune{}
	hits = 0
	hg = NewHashGenerator(prefix)
	for hits < 8 {
		hash := hg.next()
		// Looking for 5 zeros, each zero is 4 bits, we need 20 bits = 2.5 bytes
		if hash[0] == 0 && hash[1] == 0 && hash[2]&mask == 0 {
			x := hex.EncodeToString(hash[:])
			if x[5] < byte('0') || x[5] > byte('7') {
				continue
			}
			idx := int(x[5] - byte('0'))
			if password[idx] == 0 {
				password[idx] = rune(x[6])
				hits++
				fmt.Printf("decrypting... %v %v %v %v\n", hg.i, x, idx, password)
			}
		}
	}
	fmt.Printf("2: %v, %v\n", string(password[:]), time.Since(t2))
}
