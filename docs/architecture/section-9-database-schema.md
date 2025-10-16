# Section 9: Database Schema

El "esquema" se define por la siguiente estructura de directorios dentro del sistema:

```plaintext
/image-share-data/
├── raw_images/
│   └── photo_from_guest.jpg  // Staging area for new uploads, pre-processing
│
├── display_images/
│   └── a3f2b8c1-9d4e-4f6a-8c2b-1e3d5f7a9b0c.jpg // Processed, public-facing images
│
└── failed_images/
    └── corrupted_image.png   // Images that failed processing are moved here
```

---