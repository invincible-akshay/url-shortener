package handlers

import (
	// "fmt"
	"../storages"
	"log"
	"os"
	"path/filepath"
	"testing"
)

func EncodeURLs(b *testing.M) {

	dir, err1 := os.Getwd()
	if err1 != nil {
		log.Println(err1)
	}
	storage1 := &storages.Filesystem{}
	setupStorage(storage1, dir, "1")
	storage2 := &storages.Filesystem{}
	setupStorage(storage2, dir, "2")
	storage3 := &storages.Filesystem{}
	setupStorage(storage3, dir, "3")

	count := 10
	for i := 0; i < count; i++ {
		storage1.SaveCustom("url", RandomString(5, lowerAlphabets))
		storage2.SaveCustom("url", RandomString(5, lowerAlphabets+upperAlphabets))
		storage3.SaveCustom("url", RandomString(5, lowerAlphabets+upperAlphabets+numbers))
	}
	RandomString(3, lowerAlphabets)
}

func setupStorage(storageObject *storages.Filesystem, dir string, version string) {
	err := storageObject.Init(filepath.Join(dir, "tmp", version))
	if err != nil {
		log.Fatal(err)
	}
}
