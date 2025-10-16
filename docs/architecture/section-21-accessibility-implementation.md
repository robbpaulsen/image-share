# Section 21: Accessibility Implementation

Para cumplir con el requisito de WCAG 2.1 Nivel AA del PRD, el frontend `upload-ui` debe adherirse a los siguientes principios:

-   **HTML Semántico:** Usar elementos nativos de HTML para su propósito previsto (`<button>`, `<label>`, `<input>`). No usar `<div>` con manejadores de eventos para simular botones.
-   **Atributos ARIA:** Usar roles y propiedades de ARIA (Accessible Rich Internet Applications) donde sea necesario. Por ejemplo, el área de mensajes de estado debe usar `aria-live="polite"` para que los lectores de pantalla anuncien los mensajes de éxito o error automáticamente.
-   **Navegación por Teclado:** Todos los elementos interactivos deben ser alcanzables y operables usando la tecla `Tab` para la navegación y las teclas `Enter`/`Espacio` para la activación. El orden del foco debe ser lógico.
-   **Gestión del Foco:** Asegurar que el foco se gestione correctamente. Por ejemplo, si aparece un mensaje de error, el foco debe moverse programáticamente hacia él para que un usuario de lector de pantalla sea consciente del mismo.
-   **Contraste de Color:** Todo el texto y los elementos de la UI deben tener una relación de contraste de al menos 4.5:1 con su fondo, como especifican las directrices de WCAG AA.

```
