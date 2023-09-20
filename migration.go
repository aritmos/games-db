package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

type ParsedRepack struct {
	Id    string `json:"num"`
	Title string `json:"title"`
	Info  string
	Date  struct {
		Date string `json:"$date"`
	} `json:"date"`
	Link      string   `json:"link"`
	Genres    []string `json:"genres"`
	Companies []string `json:"companies"`
	Langs     string   `json:"langs"`
	Size      string   `json:"size"`
}

type Repack struct {
	id        string
	title     string
	info      string
	date      string
	link      string
	genres    []string
	companies []string
	langs     string
	size      string
}

func spitInfo(parsedtitle string) (title string, info string) {
	parts := strings.SplitN(parsedtitle, " – ", 2)
	if len(parts) == 2 {
		title = parts[0]
		info = parts[1]
		return
	}
	parts2 := strings.SplitN(parsedtitle, " + ", 2)
	if len(parts2) == 2 {
		title = parts2[0]
		info = parts2[1]
		return title, info
	}
	return parsedtitle, ""
}

func create_repack(pr *ParsedRepack) *Repack {
	title, info := spitInfo(pr.Title)
	date := pr.Date.Date[:10]
	return &Repack{
		id:        pr.Id,
		title:     title,
		info:      info,
		date:      date,
		link:      pr.Link,
		genres:    pr.Genres,
		companies: pr.Companies,
		langs:     pr.Langs,
		size:      pr.Size}
}

type ParsedRepackList []ParsedRepack

func main() {
	data, os_err := os.ReadFile("repacks.json")
	check(os_err)

	var prl ParsedRepackList
	json_err := json.Unmarshal(data, &prl)
	check(json_err)

	// fmt.Printf("%+v\n", prl)

	var rl []Repack
	for _, pr := range prl {
		r := create_repack(&pr)
		rl = append(rl, *r)
	}

	for _, r := range rl[:100] {
		title := r.title
		info := r.info
		fmt.Printf("%v\n", title)
		fmt.Printf("%v\n", info)
		fmt.Printf("---\n")
	}
}
