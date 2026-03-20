# Docker Setup for EV Sales Analysis Dashboard

This guide explains how to build and run the EV Sales visualization application using Docker.

## Prerequisites

- Docker Desktop installed on your machine
- Docker Compose installed (usually comes with Docker Desktop)
- The dataset.csv file in the project directory

## Building the Docker Image

### Option 1: Using Docker Compose (Recommended)

```bash
docker-compose build
```

### Option 2: Using Docker CLI

```bash
docker build -t ev-sales-analyzer:latest .
```

## Running the Application

### Option 1: Using Docker Compose

```bash
docker-compose up
```

### Option 2: Using Docker CLI

#### On Linux/WSL2:
```bash
docker run --rm \
  --env DISPLAY=$DISPLAY \
  --volume /tmp/.X11-unix:/tmp/.X11-unix:rw \
  --volume $(pwd):/app \
  ev-sales-analyzer:latest
```

#### On Windows (with VcXsrv or similar X Server):
1. Install VcXsrv or Xming on Windows
2. Launch the X Server
3. Get your machine IP:
```bash
ipconfig
```
4. Run Docker with:
```bash
docker run --rm `
  -e DISPLAY=<your-machine-ip>:0 `
  -v ${PWD}:/app `
  ev-sales-analyzer:latest
```

#### Alternative for Windows - Using WSL2:
```bash
# In WSL2 terminal
docker run --rm \
  --env DISPLAY=$DISPLAY \
  --volume /tmp/.X11-unix:/tmp/.X11-unix:rw \
  --volume $(pwd):/app \
  ev-sales-analyzer:latest
```

## File Structure

```
ev-sales-analysis/
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker Compose configuration
├── .dockerignore          # Files to exclude from Docker image
├── graph.py               # Main application
├── dataset.csv            # Data file
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## Docker Image Details

- **Base Image**: Python 3.10 (slim)
- **System Dependencies**: tkinter, X11 utilities
- **Python Dependencies**: pandas, matplotlib, seaborn, tkinter
- **Working Directory**: /app
- **Entry Point**: python graph.py

## Environment Variables

- `DISPLAY`: X11 display socket (for GUI)

## Volumes

- `/app`: Application directory (mounted for live code updates)
- `/tmp/.X11-unix`: X11 socket (for GUI display on Linux)

## Stopping the Container

Press `Ctrl+C` in the terminal running the container.

## Rebuilding After Changes

```bash
docker-compose build --no-cache
docker-compose up
```

## Troubleshooting

### "No display" error on Windows
- Ensure X Server (VcXsrv/Xming) is running
- Verify DISPLAY variable is set correctly
- Check Windows firewall allows connections

### "Cannot connect to X display"
- On Linux/WSL2: Ensure `/tmp/.X11-unix` is properly mounted
- Check X Server is running: `echo $DISPLAY`

### Permission denied
- On Linux: Add user to docker group: `sudo usermod -aG docker $USER`
- Log out and back in for changes to take effect

## Notes

- The application requires a display server (X11) to render the GUI
- Data file (dataset.csv) must be in the working directory
- All changes to code are reflected immediately (volume mount)
