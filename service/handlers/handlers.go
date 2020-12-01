// Package handlers provides HTTP request handlers.
package handlers

import (
	"crypto/rand"
	"fmt"
	"net/http"

	"../storages"
)

const (
	lowerAlphabets = "abcdefghijklmnopqrstuvwxyz"
	upperAlphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	numbers = "0123456789"
)

//type Page struct {
//	Title string
//	Body  []byte
//}
//
//func loadPage(title string) (*Page, error) {
//	filename := title + ".txt"
//	body, err := ioutil.ReadFile("../static/" + filename)
//	if err != nil {
//		return nil, err
//	}
//	return &Page{Title: title, Body: body}, nil
//}
//
//func EncodeHandler(storage storages.IStorage) http.Handler {
//	handleFunc := func(w http.ResponseWriter, r *http.Request) {
//		if url := r.PostFormValue("url"); url != "" {
//			w.Write([]byte(storage.Save(url)))
//		}
//	}
//
//	return http.HandlerFunc(handleFunc)
//}

//func EncodeHandlers(w http.ResponseWriter, r *http.Request) {
//	// title := r.URL.Path[len("/edit/"):]
//	title := "EncodeVersion1"
//	p, err := loadPage(title)
//	if err != nil {
//		p = &Page{Title: title}
//	}
//	fmt.Fprintf(w, "<h1>Editing %s</h1>"+
//		"<form action=\"/save/%s\" method=\"POST\">"+
//		"<textarea name=\"body\">%s</textarea><br>"+
//		"<input type=\"submit\" value=\"Save\">"+
//		"</form>",
//		p.Title, p.Title, p.Body)
//}

// RandomString ...
func RandomString(length int, alphabet string) string {
	bytes := make([]byte, length)
	rand.Read(bytes)
	for i, b := range bytes {
		bytes[i] = alphabet[b%byte(len(alphabet))]
	}
	return string(bytes)
}

func EncodeHandlers(storage storages.IStorage) http.Handler {
	handleFunc := func(w http.ResponseWriter, r *http.Request) {
		if err := r.ParseForm(); err != nil {
			fmt.Fprintf(w, "ParseForm() err: %v", err)
			return
		}

		fmt.Fprintf(w, "POST request successful \n\n")

		url := r.PostFormValue("url")
		version := r.PostFormValue("version")
		var res = ""
		if url != "" {
			switch version {
			case "2":
				res = storage.SaveCustom(url, RandomString(3, lowerAlphabets))
			case "3":
				res = storage.SaveCustom(url, RandomString(5, lowerAlphabets))
			case "4":
				res = storage.SaveCustom(url, RandomString(5, numbers+lowerAlphabets+upperAlphabets))
			default:
				res = storage.Save(url)
			}
			// res = storage.Save(url)
			// w.Write([]byte(storage.Save(url)))
		}
		newURL := "http://localhost:8080/red" + res
		fmt.Fprintf(w, "Query URL = %s\n\n", url)
		fmt.Fprintf(w, "Encoded URL = %s\n", newURL)

		// TODO: Create a HTTP page to display the result URL.
		//tmpStr := "<a href=\""+newURL+"\">Visit " + url + "!</a>"
		//fmt.Fprintf(w, tmpStr)
	}
	return http.HandlerFunc(handleFunc)
}

// func EncodeHandlers(w http.ResponseWriter, r *http.Request) {
//	if err := r.ParseForm(); err != nil {
//		fmt.Fprintf(w, "ParseForm() err: %v", err)
//		return
//	}
//	fmt.Fprintf(w, "POST request successful")
//
//	url := r.PostFormValue("url")
//	if url != "" {
//		w.Write([]byte(storage.Save(url)))
//	}
//
//	fmt.Fprintf(w, "URL = %s\n", url)
//	fmt.Fprintf(w, "Address = %s\n", address)
// }

func DecodeHandler(storage storages.IStorage) http.Handler {
	handleFunc := func(w http.ResponseWriter, r *http.Request) {
		code := r.URL.Path[len("/dec/"):]

		url, err := storage.Load(code)
		if err != nil {
			w.WriteHeader(http.StatusNotFound)
			w.Write([]byte("URL Not Found. Error: " + err.Error() + "\n"))
			return
		}

		w.Write([]byte(url))
	}

	return http.HandlerFunc(handleFunc)
}

func RedirectHandler(storage storages.IStorage) http.Handler {
	handleFunc := func(w http.ResponseWriter, r *http.Request) {
		code := r.URL.Path[len("/red/"):]

		url, err := storage.Load(code)
		fmt.Printf("r.URL.Path: %s | code: %s | url: %s \n", r.URL.Path, code, url)
		if err != nil {
			w.WriteHeader(http.StatusNotFound)
			w.Write([]byte("URL Not Found. Error: " + err.Error() + "\n"))
			return
		}

		// http.Redirect(w, r, url, 307)
		w.Write([]byte("<head> \n  <meta http-equiv=\"Refresh\" content=\"0; " +
			"URL=" + url + "\">\n</head>"))
	}

	return http.HandlerFunc(handleFunc)
}
