# Section 13: Development Workflow

### **13.1 Local Development Setup (Corregido con `uv`)**

**Prerequisites**
```bash
# 1. uv
uv --version
# 2. Ansible (Opcional)
ansible --version
```

**Initial Setup**
```bash
# 1. Clonar repo y navegar a apps/api
# 2. Crear entorno virtual
uv venv
# 3. Activar entorno
source .venv/bin/activate
# 4. Instalar dependencias
uv pip install -r requirements.txt
```

**Development Commands**
```bash
# Iniciar servidor de desarrollo
uvicorn apps.api.main:app --reload
# Ejecutar pruebas
pytest
```

### **13.2 Environment Configuration**

**Required Environment Variables**
```bash
# ---
# --- Backend (.env en apps/api) ---
LOG_LEVEL="INFO"
PHOTO_DIR_DISPLAY="/image-share-data/display_images"
PHOTO_DIR_RAW="/image-share-data/raw_images"
PHOTO_DIR_FAILED="/image-share-data/failed_images"

# ---
# --- Configuración a Nivel de Sistema (en el Raspberry Pi) ---
# WIFI_SSID="ImageShare-Party"
```

---