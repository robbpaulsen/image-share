# Section 6: Components

### **Lista de Componentes**

**1. Guest Upload UI (Frontend)**
-   **Responsibility:** Proporcionar una interfaz web simple y optimizada para móviles que permita a los invitados seleccionar y subir sus fotos. Muestra mensajes de éxito o error.
-   **Key Interfaces:** Interactúa con el endpoint `POST /api/upload` de la API.
-   **Dependencies:** Image-Share API.
-   **Technology Stack:** Vanilla JavaScript, Custom CSS, HTML5.

**2. Carousel Display UI (Frontend)**
-   **Responsibility:** Mostrar las fotos procesadas en un carrusel a pantalla completa que avanza automáticamente. Muestra la pantalla de instrucciones cuando no hay fotos.
-   **Key Interfaces:** Interactúa con el endpoint `GET /api/photos` para obtener la lista de imágenes.
-   **Dependencies:** Image-Share API.
-   **Technology Stack:** Vanilla JavaScript, Custom CSS, HTML5.

**3. Image-Share API (Backend)**
-   **Responsibility:** Servir las dos interfaces de usuario (Upload y Carousel). Proporcionar los endpoints de la API para la subida y recuperación de fotos.
-   **Key Interfaces:** Expone la API REST (`/health`, `/api/upload`, `/api/photos`).
-   **Dependencies:** Photo Processor, Almacenamiento en Filesystem.
-   **Technology Stack:** Python, FastAPI, Uvicorn.

**4. Photo Processor (Backend)**
-   **Responsibility:** Procesar las imágenes recién subidas. Esto incluye validar el formato, corregir la orientación (EXIF), generar un UUID como nuevo nombre y mover el archivo al directorio público.
-   **Key Interfaces:** Es un componente interno del backend, invocado por la API tras una subida exitosa. Interactúa directamente con el sistema de archivos.
-   **Dependencies:** Almacenamiento en Filesystem.
-   **Technology Stack:** Python, Pillow.

### **Diagrama de Componentes (Diagrama de Contenedores C4)**
```mermaid
C4Container
title Diagrama de Contenedadores para el Sistema Image-Share

Person(guest, "Invitado", "Un asistente al evento con un smartphone.")

System_Boundary(c1, "Sistema Image-Share (en Raspberry Pi)") {
    Container(upload_ui, "UI de Subida", "Vanilla JS", "Proporciona la interfaz web para que los invitados suban fotos.")
    Container(carousel_ui, "UI del Carrusel", "Vanilla JS", "Renderiza el carrusel de fotos en un navegador en modo kiosco.")
    Container(api, "Servidor Web y API", "Python/FastAPI", "Sirve las UIs y provee la API REST para subidas y listados.")
    Container(processor, "Procesador de Fotos", "Python/Pillow", "Componente interno para validar, renombrar y orientar imágenes.")
    ContainerDb(storage, "Almacenamiento de Fotos", "Filesystem (ext4)", "Almacena los archivos de imagen finales listos para mostrar.")
}

System_Ext(display, "Pantalla HDMI", "Pantalla externa que muestra el carrusel.")

Rel(guest, upload_ui, "Usa", "HTTPS")
Rel(upload_ui, api, "Llama a la API", "JSON/HTTP")
Rel(api, processor, "Dispara el procesamiento", "Llamada interna")
Rel(processor, storage, "Escribe en")
Rel(api, storage, "Lee de")
Rel(carousel_ui, api, "Llama a la API", "JSON/HTTP")
Rel(carousel_ui, display, "Se muestra en")
```

---