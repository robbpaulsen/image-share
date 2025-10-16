# Section 10: Frontend Architecture

### **10.1 Component Architecture**

**Component Organization**
```text
/upload-ui/
├── index.html              # El punto de entrada HTML
├── js/
│   ├── app.js              # Lógica principal de la aplicación
│   └── components/         # Módulos de UI reutilizables (ej. Uploader.js)
│       └── Uploader.js
├── css/
│   └── style.css           # Estilos principales
└── assets/
    └── ...                 # Imágenes, iconos, etc.
```

**Component Template (Example)**
```typescript
// Fichero: /js/components/Uploader.js

export function Uploader(rootElement, api) {
  const fileInput = rootElement.querySelector('input[type="file"]');
  const submitButton = rootElement.querySelector('button');
  const statusMessage = rootElement.querySelector('.status');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const file = fileInput.files[0];
    if (!file) return;

    submitButton.disabled = true;
    statusMessage.textContent = 'Subiendo...';

    try {
      await api.uploadPhoto(file);
      statusMessage.textContent = '¡Éxito!';
    } catch (error) {
      statusMessage.textContent = `Error: ${error.message}`;
    } finally {
      submitButton.disabled = false;
    }
  };

  submitButton.addEventListener('click', handleSubmit);
}
```

### **10.2 State Management Architecture**

**State Structure**
```typescript
// Fichero: /carousel-ui/js/app.js

let photos = []; 
let currentIndex = 0;
let isLoading = true; 
let error = null; 

function setPhotos(newPhotos) {
  photos = newPhotos;
  isLoading = false;
  render();
}
```

**State Management Patterns**
-   **Estado Local del Módulo:** El estado se encapsula dentro del archivo/módulo de JavaScript que lo necesita.
-   **Flujo de Datos Unidireccional (Simplificado):** Las acciones del usuario o las respuestas de la API llaman a funciones que actualizan las variables de estado.
-   **El Estado como "Fuente de la Verdad":** La UI es siempre un reflejo del estado actual contenido en las variables.

### **10.3 Routing Architecture**

**Route Organization**
```text
El enrutamiento es manejado por el servidor backend:

- / (ruta raíz): Sirve el archivo `index.html` de la UI de Subida (`upload-ui`).

- /display: Sirve el archivo `index.html` de la UI del Carrusel (`carousel-ui`).
```

**Protected Route Pattern**
```typescript
// No aplicable.
```

### **10.4 Frontend Services Layer**

**API Client Setup**
```typescript
// Fichero: /js/services/api.js

const BASE_URL = ''; 

export const ApiService = {
  async getPhotos() {
    const response = await fetch(`${BASE_URL}/api/photos`);
    if (!response.ok) {
      throw new Error('No se pudo obtener la lista de fotos.');
    }
    return response.json();
  },

  async uploadPhoto(photoFile) {
    const formData = new FormData();
    formData.append('photo', photoFile);

    const response = await fetch(`${BASE_URL}/api/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Error desconocido' }));
      throw new Error(errorData.detail || 'Error al subir la foto.');
    }
    return response.json();
  },
};
```

---