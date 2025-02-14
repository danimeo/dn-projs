package main

import (
	"fmt"
	"net/http"

	"gocv.io/x/gocv"
)

// Handler function to serve MJPEG stream
func streamHandler(w http.ResponseWriter, r *http.Request) {
	// Set appropriate headers for MJPEG streaming
	w.Header().Set("Content-Type", "multipart/x-mixed-replace; boundary=frame")

	// Open the video capture device
	webcam, err := gocv.VideoCaptureDevice(0) // 0 for default camera
	if err != nil {
		http.Error(w, "Error opening video capture device", http.StatusInternalServerError)
		return
	}
	defer webcam.Close()

	// Create an image matrix to hold frames
	img := gocv.NewMat()
	defer img.Close()

	// Write MJPEG stream
	for {
		if ok := webcam.Read(&img); !ok {
			fmt.Println("Error reading from webcam")
			return
		}
		if img.Empty() {
			continue
		}

		// Encode frame as JPEG
		buf := gocv.NewMat()
		defer buf.Close()
		if err := gocv.IMEncode(".jpg", img, &buf); err != nil {
			fmt.Println("Error encoding frame:", err)
			return
		}

		// Write JPEG frame to response
		w.Write([]byte("--frame\r\n"))
		w.Write([]byte("Content-Type: image/jpeg\r\n\r\n"))
		w.Write(buf.GetBytes())
		w.Write([]byte("\r\n"))
		w.(http.Flusher).Flush() // Ensure the data is sent immediately
	}
}

func main() {
	// Set up the HTTP server
	http.HandleFunc("/video", streamHandler)
	fmt.Println("Streaming server started at http://localhost:8080/video")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Println("Error starting server:", err)
	}
}
