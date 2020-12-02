package storages

import (
	"log"
	"os"
	"path/filepath"
	"testing"
)

func BenchmarkCode(b *testing.B) {
	dir, err := os.Getwd()
	if err != nil {
		log.Println(err)
	}
	// fmt.Println(path)
	// dir, _ := homedir.Dir()
	storage := &Filesystem{}
	// storage.Init(dir)
	storage.Init(filepath.Join(dir, "tmp"))

	for i := 0; i < b.N; i++ {
		storage.Code()
	}
}
