# User Interface Design Goals

## Overall UX Vision

The Image-Share interface embodies **radical simplicity** - eliminating every possible point of friction between "guest arrives at event" and "guest's photo appears on screen." The design philosophy is **invisible technology**: guests should feel like they're simply sharing to a "magic screen," not interacting with a technical system.

**Two distinct user experiences must coexist:**

1. **Guest Upload Interface (Mobile):** Brutally minimal, optimized for one-handed smartphone use in chaotic social environments (dim lighting, distraction, holding drinks). Large touch targets, minimal text, instant feedback.

2. **Carousel Display (Large Screen):** Ambient, elegant, and celebratory. Photos are the hero—UI chrome is minimal or absent. Design evokes "living memory wall" rather than "slideshow presentation."

**Assumption:** No venue/staff admin interface is in MVP scope—configuration happens via file/SSH pre-event.

## Key Interaction Paradigms

**Mobile Upload Experience:**
- **Progressive Web App (PWA) principles** without formal PWA installation—works like native app from browser
- **Single-purpose interaction model:** Landing page immediately presents "Upload Photo" as primary CTA
- **Optimistic UI:** Show upload success immediately, don't wait for backend confirmation (assume success, handle failures gracefully)
- **Ambient awareness:** If possible, show small "X photos in carousel" counter to create social proof

**Carousel Display Experience:**
- **Zero-interaction design:** Display never requires touch, mouse, or remote control input
- **Graceful photo transitions:** Smooth crossfade or slide transitions (not jarring cuts) with 7-second hold time
- **Contextual states:** Display adapts based on system state (no photos yet vs. active carousel vs. error states)
- **Unattended operation:** Can run for 6+ hours without intervention, degradation, or visual artifacts

**Assumption:** No gesture controls, voice commands, or interactive display features in MVP—pure passive viewing.

## Core Screens and Views

**Mobile Interface:**
1. **Landing/Upload Page** - Primary screen with upload CTA, connection instructions if needed, visual feedback on upload status
2. **Upload Confirmation** - Brief success state showing estimated time to display appearance
3. **Error/Retry Page** - Handles upload failures, file size issues, unsupported formats (edge case, but needs design)

**Display Interface:**
1. **Instruction Screen (No Photos State)** - QR code, Wi-Fi SSID, URL, visual instructions for first-time guests
2. **Carousel Screen (Active State)** - Full-screen photo display with minimal/no UI chrome, smooth transitions
3. **System Status Screen (Error State)** - Visible but non-alarming error message if system encounters issues (e.g., "Waiting for photos to process...")

**Assumption:** No admin/configuration screens for venue staff—this is handled outside the UI.

## Accessibility: WCAG AA

**Target Level:** WCAG 2.1 Level AA compliance for upload interface

**Rationale:**
- Event guests include users with diverse accessibility needs (visual impairments, motor challenges, cognitive differences)
- Level AA is industry standard for public-facing web applications and achievable without architectural complexity
- Primary interaction (photo upload) is inherently visual, but supporting features (text labels, keyboard navigation, sufficient contrast) must be accessible

**Specific Considerations:**
- Large touch targets (minimum 44×44px per WCAG guidelines) for upload buttons
- Sufficient color contrast for text and UI elements (4.5:1 minimum)
- Screen reader support for upload flow (semantic HTML, ARIA labels where needed)
- Keyboard navigation support for guests using alternative input devices

**Assumption:** Carousel display accessibility is not prioritized (it's ambient/passive viewing, not interactive). Focus accessibility investment on upload interface.

## Branding

**Visual Style:** Clean, modern, celebratory—evokes "event photography" without being overly formal

**Color Palette:**
- **Primary:** Warm, inviting tones (soft blues, friendly greens) that feel celebratory without being garish
- **Assumption:** No existing brand guidelines—need to establish Image-Share brand identity or make it white-label/customizable per venue

**Typography:**
- Clean, highly legible sans-serif (system fonts: -apple-system, Roboto) for zero load time and maximum compatibility
- Large font sizes for mobile (18px+ for body text) to ensure readability in varied lighting

**Tone:**
- Friendly and encouraging: "Share your photos!" not "Upload files"
- Casual, not corporate: "Your photo is on the way!" not "Upload successful"

**Logo/Branding Placement:**
- **Assumption:** Minimal Image-Share branding on interfaces—venues may want to co-brand or white-label
- QR code and instruction screen could include venue's custom logo or event name

**Open Question:** Should this be white-label (venues can customize branding) or branded as "Image-Share powered"? This affects marketing strategy.

## Target Device and Platforms: Web Responsive

**Primary Target:** Mobile web browsers (iOS Safari, Android Chrome)
- Smartphone-optimized responsive design (320px - 428px widths)
- Touch-first interaction model
- Progressive enhancement for older devices

**Secondary Target:** Desktop/tablet browsers (for testing, edge cases where guests use laptops)
- Upload interface scales to larger screens but maintains mobile-first design patterns

**Display Output:** Desktop browsers in kiosk mode (Chromium on Raspberry Pi)
- Full-screen carousel on HDMI-connected displays
- Supports resolutions up to 4K, optimized for common formats (1920×1080, 3840×2160)

**Assumption:** No native mobile apps (iOS/Android) in scope—PWA via browser only. This avoids app store friction and development complexity.

---
