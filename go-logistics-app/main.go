package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

type StatusResponse struct {
	Service string `json:"service"`
	Status  string `json:"status"`
	Version string `json:"version"`
}

func statusHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	response := StatusResponse{
		Service: "Logistics API",
		Status:  "Healthy",
		Version: "1.0.0",
	}
	json.NewEncoder(w).Encode(response)
}

func main() {
	http.HandleFunc("/status", statusHandler)
	
	port := ":8080"
	fmt.Printf("Logistics microservice starting on port %s\n", port)
	if err := http.ListenAndServe(port, nil); err != nil {
		log.Fatalf("Server failed to start: %v", err)
	}
}
