# Architecture Overview

## Core Components

### 1. Flight Dynamics
- **PyTorch-based 3DOF/6DOF physics** for simulating aircraft dynamics.
- **Quaternion math** for avoiding gimbal lock.

### 2. Control System
- **LQRI-PID controller** for combining neural network predictions with classical control.
- **ONNX runtime** for cross-platform inference.

### 3. Data Pipeline
- **Polars** for high-performance data handling.
- **Directus** for logging and analyzing flight data.

### 4. Containerization
- **Podman** for zero-trust deployment.
- **Nginx** for rate limiting and caching.
- **Fail2ban** for intrusion prevention.

## Data Flow

1. **Flight Dynamics**: Simulates aircraft state.
2. **LQRI-PID Controller**: Computes control outputs.
3. **Directus**: Logs flight data for analysis.
4. **Prometheus/Grafana**: Monitors system performance.

## Zero-Trust Architecture

### Networks
- **app-net**: Flight dynamics and control.
- **db-net**: Directus database.
- **nginx-net**: Public-facing reverse proxy.

### Security
- **Nginx rate limiting** to prevent abuse.
- **Fail2ban** to block malicious activity.
- **Isolated networks** for zero-trust security.

## Deployment

### Prerequisites
- Python 3.11+
- Podman
- UV (Python package manager)

### Setup
```bash
uv pip install -e .
podman-compose -f config/podman-compose.yml up -d
