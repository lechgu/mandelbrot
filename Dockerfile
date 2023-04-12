FROM golang:alpine as build

WORKDIR /app

COPY . .
RUN go build -o mandelbrot main.go

FROM scratch
COPY --from=build /app/mandelbrot /bin/

ENV PORT=80

ENTRYPOINT ["/bin/mandelbrot"]