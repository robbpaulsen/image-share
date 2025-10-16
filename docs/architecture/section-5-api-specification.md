# Section 5: API Specification

### **REST API Specification (OpenAPI 3.0)**
```yaml
openapi: 3.0.0
info:
  title: Image-Share API
  version: 1.0.0
  description: |-
    API para el sistema de agregación de fotos offline Image-Share.
    Esta es una API simple y sin autenticación que se ejecuta en una red local aislada.
servers:
  - url: http://10.0.17.1
    description: Servidor del dispositivo local
paths:
  /health:
    get:
      summary: Chequeo de Salud del Sistema
      description: Proporciona el estado operativo del servidor.
      responses:
        '200':
          description: El sistema está funcionando correctamente.
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "ok"
                  timestamp:
                    type: string
                    format: date-time
  /api/photos:
    get:
      summary: Obtener Todas las Fotos
      description: Recupera una lista de todas las fotos procesadas, ordenadas cronológicamente.
      responses:
        '200':
          description: Una lista de objetos de Foto.
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Photo'
  /api/upload:
    post:
      summary: Subir una Foto
      description: Sube un archivo de foto para ser procesado y mostrado en el carrusel.
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                photo:
                  type: string
                  format: binary
                  description: "El archivo de foto a subir (formatos aceptados: JPEG, PNG, HEIC)."
      responses:
        '200':
          description: Foto subida con éxito.
        '400':
          description: Petición incorrecta (ej. formato de archivo inválido).
        '413':
          description: Archivo demasiado grande (límite de 25MB).
components:
  schemas:
    Photo:
      type: object
      description: Representa una sola foto procesada.
      properties:
        id:
          type: string
          description: El UUID único de la foto.
          example: "a3f2b8c1-9d4e-4f6a-8c2b-1e3d5f7a9b0c.jpg"
        url:
          type: string
          description: La ruta URL para acceder a la imagen.
          example: "/images/a3f2b8c1-9d4e-4f6a-8c2b-1e3d5f7a9b0c.jpg"
        createdAt:
          type: string
          format: date-time
          description: La fecha y hora en formato ISO 8601 de cuándo se procesó la foto.
```

---