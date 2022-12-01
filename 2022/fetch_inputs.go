package main

import (
    "net/http"
	// "bufio"
	"fmt"
	"log"
	"os"
    "io"
	"strconv"
	"time"
)

var TEMPLATE string = "https://adventofcode.com/2022/day/%s/input"
var COOKIE_FILE string = ".session"
var OUTDIR string = "inputs"


func readCookie(filename string, cookiename string) http.Cookie {
    b, err := os.ReadFile(filename)
    if err != nil {
        log.Fatal(err)
    }

    return http.Cookie{Name: cookiename, Value: string(b)}
}

func main() {
	day := os.Args[1]
    dayInt, err := strconv.Atoi(day)
    if err != nil {
        log.Fatal(err.Error())
    }
	t0 := time.Now()

	fmt.Printf("Reading cookie from %s ...\n", COOKIE_FILE)
    cookie := readCookie(COOKIE_FILE, "session")
    fmt.Println(cookie.Value)

    url := fmt.Sprintf(TEMPLATE, day)
	fmt.Printf("Reading from %s ...\n", url)

    req, err := http.NewRequest("GET", url, nil)
    if err != nil {
        log.Fatalf("Got error %s", err.Error())
    }
    req.AddCookie(&cookie)
    client := http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        log.Fatalf("Got error %s", err.Error())
    }
    defer resp.Body.Close()

    fmt.Printf("StatusCode: %d\n", resp.StatusCode)

    if resp.StatusCode != http.StatusOK {
        log.Fatal("Status not OK") 
    }

    body, err := io.ReadAll(resp.Body)
    if err != nil {
        log.Fatal(err)
    }
    outpath := fmt.Sprintf("%s/day%02d.txt", OUTDIR, dayInt)
    fmt.Println("Writing to %s...", outpath)
    os.WriteFile(outpath, body, 0644)

    fmt.Println("Done!")

	// file, err := os.Open(filename)
	// if err != nil {
	// 	log.Fatal(err)
	// }
	// defer file.Close()

	// var depths []int
	// scanner := bufio.NewScanner(file)
	// for scanner.Scan() {
	// 	if d, err := strconv.Atoi(scanner.Text()); err != nil {
	// 		log.Fatal(err)
	// 	} else {
	// 		depths = append(depths, d)
	// 	}
	// }

	// if err := scanner.Err(); err != nil {
	// 	log.Fatal(err)
	// }

	fmt.Printf("  took %v\n", time.Since(t0))
}
