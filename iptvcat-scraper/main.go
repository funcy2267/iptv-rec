package main

import (
	app "iptvcat-scraper/pkg"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"github.com/gocolly/colly"
)

const iptvCatDomain = "iptvcat.com"
const iptvCatURL = "https://" + iptvCatDomain
const aHref = "a[href]"

func writeToFile() {
	streamsAll, err := json.Marshal(app.Streams.All)
	//streamsCountry, err := json.Marshal(app.Streams.ByCountry)
	if err != nil {
		fmt.Println("error:", err)
	}
	ioutil.WriteFile("data/all-streams.json", streamsAll, 0644)
	//ioutil.WriteFile("data/all-by-country.json", streamsCountry, 0644)
}

func main() {
	var searchQuery = strings.ToLower(strings.ReplaceAll(os.Args[1], " ", "_"))
	c := colly.NewCollector(
		colly.AllowedDomains(iptvCatDomain),
	)

	c.OnResponse(func(r *colly.Response) {
		fmt.Println("Visited", r.Request.URL)
	})

	//c.OnHTML(aHref, app.HandleFollowLinks(c))
	c.OnHTML(app.GetStreamTableSelector(), app.HandleStreamTable(c))

	c.OnScraped(func(r *colly.Response) {
		fmt.Println("Finished", r.Request.URL)
	})

	c.OnError(func(r *colly.Response, err error) {
		fmt.Printf("Error: %d %s\n", r.StatusCode, r.Request.URL)
	})

	c.Visit(iptvCatURL+"/s/"+searchQuery)
	c.Wait()
	writeToFile()
}
