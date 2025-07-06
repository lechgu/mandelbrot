# Mandelbrot

**Mandelbrot** is a service for generating Mandelbrot set images through a JSON API. The service allows customizable image parameters and can be run as a Python app using Uvicorn or as a Docker container (Dockerfile provided).

<p align="center">
  <img src="walk.png" alt="Mandelbrot walk animation" />
</p>

## Features

- JSON API for generating Mandelbrot set images
- Customizable image size, bounds, and iteration depth
- Can run locally with Python/Uvicorn or as a Docker container

## Getting Started

### Run Locally (Python)

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the service:

   ```bash
   uvicorn mandelbrot_service:app --host 0.0.0.0 --port 8080
   ```

   > Replace `mandelbrot_service:app` with the correct module and app name if different.

4. Access the service at:

   ```
   http://localhost:8080
   ```

### Run with Docker

1. Build the Docker image:

   ```bash
   docker build -t mandelbrot .
   ```

2. Run the container:

   ```bash
   docker run -p 8080:80 mandelbrot
   ```

3. Access the service at:

   ```
   http://localhost:8080
   ```

## API

### `POST /generate`

Generates a Mandelbrot set image.

#### Request body (JSON)

```json
{
  "width": 640,
  "height": 480,
  "x_min": -2.0,
  "x_max": 1.0,
  "y_min": -1.5,
  "y_max": 1.5,
  "max_iter": 1000
}
```
