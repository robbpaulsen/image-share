# Section 4: Data Models

### **Photo Model**

**Purpose:**
Represents a single photo uploaded by a guest. This is the central data entity of the entire system. Its structure will be used in API responses and frontend state management.

**Key Attributes:**
-   `id: string` - The unique UUID of the photo, which also serves as its filename on the server.
-   `url: string` - The URL path to retrieve the full-resolution image for display in the carousel.
-   `createdAt: string` - The ISO 8601 timestamp indicating when the photo was processed. This is crucial for sorting the carousel chronologically.

### **TypeScript Interface**
```typescript
interface Photo {
  id: string;
  url: string;
  createdAt: string;
}
```

### **Relationships**
-   No direct relationships are defined in the MVP. Conceptually, a Photo "belongs to" an Event, but an Event is not a managed data entity within the system itself.

---