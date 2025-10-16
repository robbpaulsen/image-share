# Section 15: Security and Performance

### **15.1 Security Requirements**

**Frontend Security:**
-   **CSP Headers:** `default-src 'self'`
-   **XSS Prevention:** No se renderiza contenido de usuario como HTML.
-   **Secure Storage:** N/A.

**Backend Security:**
-   **Input Validation:** Estricta validación de tipo y tamaño de archivo.
-   **Rate Limiting:** N/A para MVP.
-   **CORS Policy:** N/A para despliegue same-origin.

**Authentication Security:** N/A.

### **15.2 Performance Optimization (Corregido)**

**Frontend Performance:**
-   **Bundle Size Target:** `< 50KB (JS + CSS)`
-   **Loading Strategy:** Carga mínima con scripts `defer`.
-   **Caching Strategy:** Cabeceras de cache HTTP estándar.

**Backend Performance:**
-   **Response Time Target:** Latencia total (subida a carrusel) de **≤ 10 segundos**.
-   **Database Optimization:** N/A (Filesystem). La estrategia de acceso a datos se define en la sección de Arquitectura de Base de Datos, donde se especifica que el script `extract-photos.sh` **debe encriptar el archivo ZIP de salida con una contraseña** para proteger la privacidad de los invitados.
-   **Caching Strategy:** Cache en memoria por 5 segundos para `GET /api/photos`.

---