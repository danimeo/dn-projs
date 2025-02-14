package main

import (
	"fmt"
	"net/http"
)

// handler function that will handle requests to the root URL
func handler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello, World!")
}

func main() {
	// Register the handler function for the root URL path
	http.HandleFunc("/", handler)

	// Start the server on port 8080
	fmt.Println("Server is starting on port 8080...")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Println("Error starting server:", err)
	}
}
