# 3DOF_MODEL v2

A **modernized 3DOF flight dynamics and control system** built with **PyTorch, ONNX, Pydantic, Polars, and Directus**, designed for **real-time simulation, embedded deployment, and data analysis**.

![3DOF Model Architecture](https://via.placeholder.com/800x400?text=3DOF+Model+Architecture)

---

## **🚀 Features**
- **PyTorch-based 3DOF/6DOF flight dynamics** with quaternion math.
- **ONNX runtime** for cross-platform inference.
- **Pydantic** for data validation and serialization.
- **Polars** for high-performance data handling.
- **Directus** for real-time data logging and analysis.
- **Zero-trust architecture** with Podman, Nginx, and Fail2ban.
- **Prometheus + Grafana** for monitoring and observability.

---

## **📦 Project Structure**
```
.
├── README.md
├── config/
│   ├── podman-compose.yml
│   ├── Containerfile
│   ├── .gitlab-ci.yml
│   ├── nginx.conf
│   └── fail2ban/
├── data/
│   └── telemetry.json
├── docs/
│   └── architecture.md
├── pyproject.toml
├── uv.lock
├── __init__.py
├── main.py
├── scripts/
│   ├── generate_onnx_model.py
│   └── run_simulation.py
├── src/
│   ├── __init__.py
│   ├── vector.py
│   ├── environment.py
│   ├── aerodynamics.py
│   ├── propulsion.py
│   ├── onnx_interpreter.py
│   ├── lqri_pid.py
│   ├── flight_dynamics.py
│   ├── schemas.py
│   └── directus_client.py
└── tests/
    ├── unit/
    ├── integration/
    └── system/
```

---

## **🛠 Setup**

### **Prerequisites**
- **Python 3.11+**
- **Podman** (or Docker)
- **UV** (Python package manager)

### **Installation**
1. **Clone the repository**:
   ```bash
   git clone https://github.com/RAliane/3DOF_MODEL_V2.git
   cd 3DOF_MODEL_V2
   ```

2. **Install dependencies**:
   ```bash
   uv pip install -e .
   ```

3. **Generate a dummy ONNX model** (for testing):
   ```bash
   uv run generate_onnx
   ```

---

## **🚀 Usage**

### **Run the Simulation**
```bash
uv run run_simulation
```
This will:
- Simulate 1000 timesteps of flight dynamics.
- Log data to **Directus** and export telemetry to `data/telemetry.json`.

### **Example Output**
```
Step 0: Throttle=0.456, Elevator=0.123
Step 1: Throttle=0.478, Elevator=0.118
...
Step 999: Throttle=0.789, Elevator=-0.012
```

---

## **🧪 Testing**
Run all tests:
```bash
pytest
```
- **Unit tests**: Core logic and classes.
- **Integration tests**: Component interactions.
- **System tests**: End-to-end simulation.

---

## **📊 Data Analysis**
### **Directus Dashboard**
- Access the Directus dashboard at [`http://localhost:8055`](http://localhost:8055).
- Log in with `admin@example.com` / `admin`.
- View logged flight data in the `flight_logs` collection.

### **Prometheus + Grafana**
- **Prometheus**: [`http://localhost:9090`](http://localhost:9090)
- **Grafana**: [`http://localhost:3000`](http://localhost:3000)
- Use these tools to monitor system performance and flight metrics.

---

## **🐳 Deployment**

### **Build and Run Containers**
```bash
podman-compose -f config/podman-compose.yml build
podman-compose -f config/podman-compose.yml up -d
```

### **Services**
| Service      | URL                     | Description                     |
|--------------|-------------------------|---------------------------------|
| **App**      | `http://localhost:8000` | Flight dynamics API.           |
| **Directus** | `http://localhost:8055` | Data logging and analysis.     |
| **Prometheus** | `http://localhost:9090` | Metrics and monitoring.         |
| **Grafana**  | `http://localhost:3000` | Dashboards and visualization.   |

---

## **🔧 Configuration**

### **Environment Variables**
Set these in your `.env` file or directly in `podman-compose.yml`:
```yaml
DIRECTUS_URL: http://db:8055
DIRECTUS_EMAIL: admin@example.com
DIRECTUS_PASSWORD: admin
```

### **Nginx**
- **Rate limiting**: 10 requests/second.
- **Caching**: Enabled for static assets.

### **Fail2ban**
- Blocks IPs after 5 failed attempts in 60 seconds.

---

## **📝 Documentation**
- **[Architecture Overview](docs/architecture.md)**: Detailed design and data flow.
- **[API Reference](docs/api.md)**: (Add this file for API endpoints.)

---

## **🤝 Contributing**
1. **Fork the repository**.
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature
   ```
3. **Commit your changes**:
   ```bash
   git commit -m "Add your feature"
   ```
4. **Push to the branch**:
   ```bash
   git push origin feature/your-feature
   ```
5. **Open a pull request**.

---

## **📜 License**
This project is licensed under the **Apache License 2.0** – see [`LICENSE.md`](LICENSE.md) for details.

---

## **📬 Contact**
For questions or feedback, reach out to [Rayan Aliane](mailto:rayan.alianel@outlook.com).

---

### **Key Improvements**
1. **Visual Appeal**: Added a placeholder for an architecture diagram.
2. **Clear Sections**: Organized into **Setup, Usage, Testing, Deployment, Configuration, Documentation, Contributing, and License**.
3. **Examples**: Included **code snippets** and **example outputs**.
4. **Tables**: Used for **service URLs** and **environment variables**.
5. **Links**: Added placeholders for **detailed documentation** and **API reference**.
6. **Contributing Guidelines**: Encourages community involvement.

---

### **How to Use This README**
1. **Replace placeholders** (e.g., `your-email@example.com`, diagram URL).
2. **Add screenshots** of Directus/Grafana dashboards if available.
3. **Extend the API reference** section as needed.
