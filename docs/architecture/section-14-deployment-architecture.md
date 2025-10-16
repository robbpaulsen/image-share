# Section 14: Deployment Architecture

### **14.1 Deployment Strategy**

**Frontend Deployment:**
-   **Platform:** N/A (Servido por el backend).
-   **Build Command:** N/A.
-   **Output Directory:** `apps/api/static/`

**Backend Deployment:**
-   **Platform:** Raspberry Pi OS Lite (64-bit).
-   **Build Command:** N/A.
-   **Deployment Method:** `git clone`, `uv pip install`, y activación de `systemd`.

### **14.2 CI/CD Pipeline**

```yaml
# Fichero: .github/workflows/ci.yaml
name: Continuous Integration
on: [push, pull_request]
jobs:
  test-and-lint:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./apps/api
    steps:
    - uses: actions/checkout@v4
    - uses: astral-sh/setup-uv@v1
      with:
        uv-version: latest
    - name: Install Dependencies
      run: uv pip install -r requirements.txt
    - name: Lint with Ruff
      run: uv run ruff check ../..
    - name: Run Backend Tests
      run: uv run pytest
```

### **14.3 Environments**

| Environment | Frontend URL | Backend URL | Purpose |
| :--- | :--- | :--- | :--- |
| **Development** | `http://localhost:8000/` | `http://localhost:8000/` | Desarrollo y pruebas en la máquina local. |
| **Staging** | `http://10.0.17.1/` | `http://10.0.17.1/` | Un Raspberry Pi dedicado para pruebas de aceptación. |
| **Production** | `http://10.0.17.1/` | `http://10.0.17.1/` | Dispositivos desplegados en los eventos. |

---