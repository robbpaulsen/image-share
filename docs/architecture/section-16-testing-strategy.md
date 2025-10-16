# Section 16: Testing Strategy

### **16.1 Testing Pyramid**

```text
           /\
          /  \
         /----
        /      \  <-- Pruebas de Integración (API)
       /--------\
      /          \ <-- Pruebas Unitarias
     /____________\ 
```

### **16.2 Test Organization**

**Frontend Tests:** Principalmente manuales para el MVP.
**Backend Tests:** En el directorio `/apps/api/tests/`.
**E2E Tests:** Checklists manuales y scripts en `/scripts/`.

### **16.3 Test Examples**

**Backend API Test (Real)**
```python
# Fichero: /apps/api/tests/test_main.py
from fastapi.testclient import TestClient
from ..main import app
client = TestClient(app)
def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

**E2E Test (Manual Checklist)**
```text
# ---
# --- Caso de Prueba E2E (Manual) ---
Feature: Subida de foto exitosa de extremo a extremo.
Pasos:
1. Conectarse a la red Wi-Fi.
2. Navegar a la IP del dispositivo.
3. Subir una imagen.
4. VERIFICAR: Mensaje de éxito en el móvil.
5. VERIFICAR: La foto aparece en el carrusel en menos de 10 segundos.
```

---