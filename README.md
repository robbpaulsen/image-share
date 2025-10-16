# Proyecto de aplicación web diseñado para que los invitados de un evento, como un cumpleaños o una fiesta, puedan compartir sus fotos fácilmente y verlas en una presentación en tiempo real. 

## Tecnologias/Frameworks/Lenguahes de Programacion usados: 
- React
- Typescript
- HTML
- CSS
- Json

## Hardware usado en el proyecto: 
- Pantalla plana de 36 pulgadas, montada en orientacion vertical 
- RaspberryPi 4B 
- Modulo de expansion X825 y X825-V2 
- Modulo de expansion UPSPack Standard con bateria lipo 

## Flujo de trabajo del servicio en el backend: 
1. El servidor es iniciado manualmente y en sitio. 
2. El servidor ya inicializado levanta un access point, el access point cuenta con accesso por invitacion via codigo QR (esta funcionalidad se documenta mas adelante, no es responsabilidad del servidor, solo debe de arrancar y levantar el acces point). 
3. Despues de 3 minutos se auto inicia la aplicacion principal, es una aplicacion web que cuenta con un frontend y un servicio como backend. 
4. El servicio inicia con dos consultas, una es revisar si el access point esta levantado y la segunda consulta es cual su direccion local acutal. Ambos datos son guardados en variables para ser usados mas adelante. 
5. Ambas consultas siempre deben de regresar los mismos datos en cada evento social, puesto que el codigo QR es comuicado por material impreso en las entradas del evento y en las mesas de los invitados en forma de tent card. Este dato es importante ya que si alguno de los datos llegase a cambiar no hay forma alguna en la que el usuario pueda ser conectado al servidor y no habria carga de imagenes. 

## Flujo de trabajo frontend: 
1. Usuario escaneo el codigo QR que se encuentra en su mesa.
2. El codigo QR contiene las credenciales del access point y el cliente es autenticado. 
3. El mismo codigo QR ya autenticado el usuario lo redirige hacia el endpoint de carga Ejemplo: ("[http://direccion.ip.local]:[puerto]/[endpoint_carga_imagen] 
4. El endpoint [endpoint_carga_imagen] instruye al usuario para cargar la o las imagenes (las cargas no tienen limite de tamano o de cantidad de imagenes. Los formatos que acepta el servicio son los estandares png, jpg, jpeg, webp, gif) 
5. El usuario escoge la imagen o imagenes las confirmar y posteriormente las carga. 
6. Con las imagenes ya cargadas, el servicio redirige al usuario al siguiente endpoint Ejemplo: "[http://direccion.ip.local]:[puerto]/[despedida_y_desconexion]" 
7. Al finalizar la carga de imagenes el usuario es desconectado. Si se quiere volver a usar el servicio para cargar mas imagenes se debe de volver a escanear el codigo QR. 

## Subprocesos del servicio backend: 
1. Hay un servicio monitoreando cada 10 segundos si hay imagenes nuevas o si no existen recursos cargados. 
2. Si no hay recursos/imagenes cargadas se sigue mostrando el contenido del endpoint Ejemplo: "[http://direccion.ip.local]:[puerto]/[carga_tu_imagen]" 
3. Si detecta recursos nuevos o cargados el servicio procede a renombrar recursivamente con un UUID (Identificador Universal Unico) todas las imagenes. 
4. Una vez renombradas, son organizadas y puestas en cola en orden alfa numerico convencional y mostradas en el endpoint Ejemplo: "[http://direccion.ip.local]:[puerto]/[display_imagenes]". Cada imagen sera mostrada un total de 7 segundos. 
5. Si el carrusel de imagenes termina y no hay nuevas imagenes este vuelve a iniciar en el mismo orden.
6. Al finaliar el evento con ayuda de un script se extraen todas las imagenes compartidas para ser comprimidas y transferidas a una unidad de almacenamiento USB y sera enviado por mensajeria al anfitrion al dia siguiente.

###### __nota: la pantalla plana en orientacion vertical todo el tiempo esta encendida mostrando en pantalla completa las imagenes que ya esten cargadas, las cuales son puestas en cola y se encuentran en el endpoint Ejemplo: "[http://direccion.ip.local]:[puerto]/[display_imagenes]" . Sino hay imagenes aun en cola la pantalla plana muestra el endpoint Ejemplo: "[http://direccion.ip.local]:[puerto]/[carga_tus_imagenes]"__

## Orden endpoints:
- El endpoint "/" , index o raiz es el del `display_images`
- `display_images` solo mostrara las imagenes no tendra opciones de carga o ninguna otra funcionalidad
- el segundo endpoint es el de `upload_images`
- solo esos dos endpoints son accesibles

## Detalles Extra:
- No hay limite de tamano de carga de una imagen
- No hay limite en cantidad de imagenes a cargar
- Solo se permiten los tipos de imagenes mas populares:
    * jpg
    * jpeg
    * png
    * gif
    * tiff
    * webp
    * bmp

## Development Setup

### Prerequisites
- Python 3.10 or higher
- uv package manager (https://github.com/astral-sh/uv)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd image-share
```

2. Create and activate a virtual environment using uv:
```bash
uv venv
```

3. Activate the virtual environment:
- On Windows (Git Bash):
```bash
source .venv/Scripts/activate
```
- On Linux/Mac:
```bash
source .venv/bin/activate
```

4. Install dependencies:
```bash
uv pip install -r apps/api/requirements.txt
```

### Running the Development Server

1. Navigate to the API directory:
```bash
cd apps/api
```

2. Start the FastAPI development server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. The API will be available at `http://localhost:8000`
   - Health check endpoint: `http://localhost:8000/health`
   - API documentation: `http://localhost:8000/docs`

### Running Tests

```bash
pytest apps/api/tests/
```
