# Section 11: Backend Architecture

### **11.1 Service Architecture**

**Controller/Route Organization**
```text
/backend/
├── main.py
├── api/
│   ├── photos.py
│   └── upload.py
├── core/
│   ├── processor.py
│   ├── models.py
│   └── repository.py
└── static/
```

**Controller Template (Example)**
```python
# Fichero: /backend/api/photos.py

from fastapi import APIRouter, HTTPException
from typing import List
from ..core.models import Photo

router = APIRouter()
PHOTO_DIR = "/image-share-data/display_images/"

@router.get("/api/photos", response_model=List[Photo], tags=["Photos"])
async def get_all_photos():
    # ... (lógica para leer archivos y devolver la lista)
    pass
```

### **11.2 Database Architecture**

**Schema Design**
```text
// No se usa SQL. El "esquema" es la estructura de directorios.
/image-share-data/
├── display_images/
├── raw_images/
└── failed_images/
```

**Data Access Layer (Repository Pattern)**
```python
# Fichero: /backend/core/repository.py

class PhotoRepository:
    def get_all_sorted_by_date(self) -> List[Photo]:
        # ... (lógica para abstraer el acceso al filesystem)
        pass

photo_repository = PhotoRepository()
```

### **11.3 Authentication and Authorization**

**Auth Flow**
```mermaid
%% No aplicable.
```

**Middleware/Guards**
```python
# No aplicable.
```

---