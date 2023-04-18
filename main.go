package main

import (
	"bufio"
	"bytes"
	"encoding/base64"
	"fmt"
	"image"
	"image/color"
	"image/png"
	"log"
	"math/cmplx"
	"net/http"
	"os"
	"strconv"

	"github.com/gin-gonic/gin"
)

const (
	xmin   = -2
	ymin   = -2
	xmax   = 2
	ymax   = 2
	width  = 1024
	height = 1024
)

func mandelbrot(z complex128) color.Color {
	const iterations = 200
	const contrast = 15

	var v complex128

	for n := uint8(0); n < iterations; n++ {
		v = v*v + z
		if cmplx.Abs(v) > 2 {
			return color.Gray{
				255 - contrast*n,
			}
		}
	}
	return color.Black
}

func generate() string {
	img := image.NewRGBA(image.Rect(0, 0, width, height))
	for r := 0; r < height; r++ {
		y := float64(r)/height*(ymax-ymin) + ymin
		for c := 0; c < width; c++ {
			x := float64(c)/width*(xmax-xmin) + xmin
			z := complex(x, y)
			img.Set(c, r, mandelbrot(z))
		}
	}
	var b bytes.Buffer
	w := bufio.NewWriter(&b)
	png.Encode(w, img)
	w.Flush()
	return base64.StdEncoding.EncodeToString(b.Bytes())
}

func main() {
	r := gin.Default()
	r.GET("/", func(ctx *gin.Context) {
		result := generate()
		ctx.String(http.StatusOK, result)
	})

	ports := os.Getenv("PORT")
	if ports == "" {
		ports = "8080"
	}
	port, err := strconv.ParseInt(ports, 10, 16)
	if err != nil {
		log.Fatalln(err)
	}

	r.Run(fmt.Sprintf(":%d", port))
}
