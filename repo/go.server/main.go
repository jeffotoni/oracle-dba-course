package main

import (
	"io"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/api/v1/user", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}

		body, err := io.ReadAll(r.Body)
		if err != nil {
			http.Error(w, "invalid body", http.StatusBadRequest)
			return
		}

		log.Printf("json recebido: %s", body)

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write(body)
	})

	log.Println("server running on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
