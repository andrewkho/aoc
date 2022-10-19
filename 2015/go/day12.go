package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"time"
)

func decodeMap(data map[string]interface{}, ignoreRed bool) int64 {
	var total int64 = 0
	for k, v := range data {
		switch v := v.(type) {
		case []interface{}:
			total += decodeList(v, ignoreRed)
		case map[string]interface{}:
			total += decodeMap(v, ignoreRed)
		case float64:
			total += int64(v)
		case string:
			if ignoreRed && v == "red" {
				return 0
			}
		default:
			log.Fatal(fmt.Sprintf("unknown type in map %v: %v, %T", k, v, v))
		}
	}
	return total
}

func decodeList(data []interface{}, ignoreRed bool) int64 {
	total := int64(0)
	for k, v := range data {
		switch v := v.(type) {
		case []interface{}:
			total += decodeList(v, ignoreRed)
		case map[string]interface{}:
			total += decodeMap(v, ignoreRed)
		case float64:
			total += int64(v)
		case string:
			// do nothing yet
		default:
			log.Fatal(fmt.Sprintf("unknown type in list %v: %v, %T", k, v, v))
		}
	}
	return total
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

	var line string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line = scanner.Text()
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	var data map[string]interface{}
	if err := json.Unmarshal([]byte(line), &data); err != nil {
		panic(err)
	}
	fmt.Printf(" took %v\n", time.Since(t0))

	t1 := time.Now()
	total := decodeMap(data, false)
	fmt.Printf("1: %v, %v\n", total, time.Since(t1))

	t2 := time.Now()
	total = decodeMap(data, true)
	fmt.Printf("2: %v, %v\n", total, time.Since(t2))
}
