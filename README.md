# 📸 Image-Share: ¡Tu Fotomatón Digital para Eventos! 🥳

Una aplicación web diseñada para que los invitados de un evento, como un cumpleaños 🎂, una boda 💍 o una fiesta 🎉, puedan compartir sus fotos fácilmente y verlas en una presentación en tiempo real.

---

## 🚀 Tecnologías y Frameworks

-   ⚛️ **React**: Para una interfaz de usuario dinámica y moderna.
-   🔷 **TypeScript**: Para un código más robusto y seguro.
-   📄 **HTML**: La estructura fundamental de la web.
-   🎨 **CSS**: Para dar vida y estilo a la aplicación.
-   📋 **JSON**: Para el intercambio de datos.

---

## 🛠️ Hardware Utilizado en el Proyecto

-   🖥️ **Pantalla Plana de 36 pulgadas**: Montada en orientación vertical para una visualización óptima.
-   🍓 **RaspberryPi 4B**: El cerebro compacto y potente de nuestro sistema.
-   🔋 **Módulos de Expansión**:
    -   `X825` y `X825-V2` para almacenamiento.
    -   `UPSPack Standard` con batería LiPo para no perder ni un solo recuerdo.

---

## ⚙️ Flujo de Trabajo del Backend

1.  ▶️ **Inicio Manual**: El servidor se inicia manualmente en el lugar del evento.
2.  📡 **Access Point**: Se levanta un punto de acceso Wi-Fi con invitación por código QR.
3.  🚀 **Autoinicio de la App**: Tras 3 minutos, la aplicación web principal (frontend + backend) se inicia automáticamente.
4.  🔍 **Verificación Inicial**: El servicio verifica el estado del access point y su dirección IP local, guardando estos datos.
5.  🔒 **Consistencia Crítica**: La IP y el nombre del access point deben ser siempre los mismos. ¡Son la clave para que los invitados se conecten a través de los códigos QR impresos!

---

## 🤳 Flujo de Trabajo del Frontend (Invitado)

1.  📱 **Escanear QR**: El invitado escanea el código QR en su mesa.
2.  🔗 **Conexión Automática**: El código QR contiene las credenciales del Wi-Fi, conectando al usuario al instante.
3.  🌐 **Redirección a la App**: Una vez conectado, el usuario es redirigido al endpoint de carga. Ejemplo: `http://direccion.ip.local:puerto/upload`.
4.  ⬆️ **Carga de Imágenes**: La interfaz guía al usuario para que suba sus fotos. ¡Sin límites de tamaño o cantidad! Se aceptan formatos como `png`, `jpg`, `jpeg`, `webp`, y `gif`.
5.  ✅ **Confirmación**: El usuario selecciona y confirma sus imágenes para la carga.
6.  👋 **Despedida**: Una vez completada la carga, se redirige al usuario a una página de agradecimiento y se desconecta.
7.  🔄 **Cargar más**: Para subir más fotos, simplemente hay que volver a escanear el código QR.

---

## 🔄 Subprocesos del Servicio Backend

1.  👀 **Monitoreo Constante**: Un servicio vigila cada 10 segundos si hay imágenes nuevas.
2.  🖼️ **Pantalla de Bienvenida**: Si no hay imágenes, la pantalla principal muestra una invitación a cargar la primera foto.
3.  🏷️ **Renombrado con UUID**: Al detectar nuevas imágenes, el servicio las renombra recursivamente con un Identificador Único Universal (UUID) para evitar conflictos.
4.  🎞️ **Carrusel en Tiempo Real**: Las imágenes renombradas se organizan y se muestran en un carrusel en el endpoint principal (`/display_images`). Cada imagen se muestra durante 7 segundos.
5.  🔁 **Loop Infinito**: Si el carrusel termina y no hay nuevas fotos, vuelve a empezar.
6.  🎁 **Recopilación Final**: Al finalizar el evento, un script extrae todas las imágenes, las comprime y las transfiere a una unidad USB para ser enviadas al anfitrión.

> 📌 **Nota Importante**: La pantalla plana siempre está encendida, mostrando el carrusel de imágenes en `http://direccion.ip.local:puerto/display_images`. Si no hay fotos, muestra la pantalla de carga `http://direccion.ip.local:puerto/upload`.

---

## 🗺️ Endpoints de la Aplicación

-   `/` o `/display_images`: Endpoint principal. Muestra el carrusel de imágenes a pantalla completa. 🎠
-   `/upload_images`: Endpoint para que los usuarios carguen sus imágenes. 📤

---

## ✨ Detalles Extra

-   ✅ **Sin límite de tamaño** de imagen.
-   ✅ **Sin límite en la cantidad** de imágenes a cargar.
-   ✅ **Formatos permitidos**: `jpg`, `jpeg`, `png`, `gif`, `tiff`, `webp`, `bmp`.

---

## 👨‍💻 Development Setup

### Prerequisites
- Python 3.10 or higher
- `uv` package manager (https://github.com/astral-sh/uv)

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd image-share
    ```

2.  Create and activate a virtual environment using `uv`:
    ```bash
    uv venv
    ```

3.  Activate the virtual environment:
    -   On Windows (Git Bash):
        ```bash
        source .venv/Scripts/activate
        ```
    -   On Linux/Mac:
        ```bash
        source .venv/bin/activate
        ```

4.  Install dependencies:
    ```bash
    uv pip install -r requirements.txt
    ```

### Running the Development Server

1.  Navigate to the API directory:
    ```bash
    cd apps/api
    ```

2.  Start the FastAPI development server:
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

3.  The API will be available at `http://localhost:8000`
    -   Health check endpoint: `http://localhost:8000/health`
    -   API documentation: `http://localhost:8000/docs`

### Running Tests

```bash
pytest apps/api/tests/
```