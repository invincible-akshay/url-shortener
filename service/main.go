package main

import (
	"log"
	"net/http"
	"os"
	"path/filepath"
	"runtime"

	"./handlers"
	"./storages"
)

func main() {
	runtime.GOMAXPROCS(runtime.NumCPU())

	dir, err1 := os.Getwd()
	if err1 != nil {
		log.Println(err1)
	}
	storage := &storages.Filesystem{}
	err := storage.Init(filepath.Join(dir, "tmp"))
	if err != nil {
		log.Fatal(err)
	}
	fileServer := http.FileServer(http.Dir("project/url-shortener/service/static")) // New code
	http.Handle("/", fileServer)
	http.Handle("/enc", handlers.EncodeHandlers(storage))
	http.Handle("/dec/", handlers.DecodeHandler(storage))
	http.Handle("/red/", handlers.RedirectHandler(storage))

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	err = http.ListenAndServe(":"+port, nil)
	if err != nil {
		log.Fatal(err)
	}
}
