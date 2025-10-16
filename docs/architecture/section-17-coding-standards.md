# Section 17: Coding Standards

### **17.1 Critical Fullstack Rules**
-   Variables de Entorno Centralizadas.
-   Abstracción del Acceso a Datos (usar Repositorio).
-   Abstracción de Llamadas a la API (usar `ApiService`).
-   No Hardcodear Rutas.
-   Manejo de Errores Estándar.

### **17.2 Naming Conventions**

| Elemento | Frontend (JS/CSS) | Backend (Python) | Ejemplo |
| :--- | :--- | :--- | :--- |
| **Variables/Funciones** | `camelCase` | `snake_case` | `getPhotos()`, `get_all_photos()` |
| **Clases/Módulos** | `PascalCase` | `PascalCase` | `ApiService.js`, `PhotoRepository` |
| **Nombres de Archivo** | `PascalCase.js` | `snake_case.py` | `Uploader.js`, `photo_repository.py` |
| **Clases de CSS** | `kebab-case` | N/A | `.main-container` |
| **Endpoints de API** | N/A | `snake_case` | `/api/photos` |

---