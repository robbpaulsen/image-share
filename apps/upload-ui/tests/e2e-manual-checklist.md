# Upload UI E2E Manual Test Checklist

**Test Environment:**
- Server running at: `http://localhost:8000/` (development) or `http://10.0.17.1/` (production)
- Tested on: [Date] by [Tester Name]

---

## Pre-requisites

- [ ] Backend API server is running
- [ ] Mobile device connected to same network (for production testing)
- [ ] Browser developer tools accessible (for console error checking)

---

## Test Cases

### 1. Page Load and Initial State

- [ ] **TC-1.1:** Navigate to `http://localhost:8000/` - page loads within 3 seconds
- [ ] **TC-1.2:** Page displays "Share Your Photo" heading
- [ ] **TC-1.3:** "Upload Photo" button is visible and properly styled
- [ ] **TC-1.4:** No JavaScript errors in browser console
- [ ] **TC-1.5:** Page is responsive at 320px viewport width
- [ ] **TC-1.6:** Page is responsive at 428px viewport width

### 2. Photo Selection Flow

- [ ] **TC-2.1:** Click "Upload Photo" button
- [ ] **TC-2.2:** Native device photo picker opens
- [ ] **TC-2.3:** Select a valid JPEG photo (<25MB)
- [ ] **TC-2.4:** Thumbnail preview appears after selection
- [ ] **TC-2.5:** Thumbnail displays correctly with proper aspect ratio
- [ ] **TC-2.6:** "Submit Photo" button appears after selection
- [ ] **TC-2.7:** No console errors during selection process

### 3. Photo Upload Success Flow

- [ ] **TC-3.1:** Click "Submit Photo" button
- [ ] **TC-3.2:** Loading indicator (spinner + "Uploading your photo...") displays
- [ ] **TC-3.3:** Submit button is disabled during upload
- [ ] **TC-3.4:** Success message displays: "Photo uploaded! It will appear on the display soon."
- [ ] **TC-3.5:** Success message has green background styling
- [ ] **TC-3.6:** "Upload Another Photo" button appears
- [ ] **TC-3.7:** No console errors during upload
- [ ] **TC-3.8:** Photo file is saved in `raw_images/` directory (backend check)

### 4. Upload Another Photo Flow

- [ ] **TC-4.1:** Click "Upload Another Photo" button
- [ ] **TC-4.2:** Form resets to initial state
- [ ] **TC-4.3:** Thumbnail preview is cleared
- [ ] **TC-4.4:** Submit button is hidden
- [ ] **TC-4.5:** Success message is cleared
- [ ] **TC-4.6:** Upload Photo button is re-enabled
- [ ] **TC-4.7:** Can select and upload a second photo successfully

### 5. Error Handling - Oversized File

- [ ] **TC-5.1:** Select a photo larger than 25MB
- [ ] **TC-5.2:** Click "Submit Photo"
- [ ] **TC-5.3:** Error message displays with red background
- [ ] **TC-5.4:** Error message mentions file size limit
- [ ] **TC-5.5:** Error message has shake animation
- [ ] **TC-5.6:** Submit button is re-enabled after error
- [ ] **TC-5.7:** Can retry with a smaller file

### 6. Error Handling - Invalid Format

- [ ] **TC-6.1:** Attempt to select a non-image file (if possible via file picker)
- [ ] **TC-6.2:** If validation occurs, error message displays
- [ ] **TC-6.3:** Error handling is graceful

### 7. Error Handling - Network Error

- [ ] **TC-7.1:** Stop the backend server
- [ ] **TC-7.2:** Attempt to upload a photo
- [ ] **TC-7.3:** Network error message displays
- [ ] **TC-7.4:** Error message is user-friendly (not technical)
- [ ] **TC-7.5:** Submit button is re-enabled
- [ ] **TC-7.6:** Restart server and verify retry works

### 8. Accessibility - Keyboard Navigation

- [ ] **TC-8.1:** Tab key moves focus to "Upload Photo" button
- [ ] **TC-8.2:** Focus indicator is visible (yellow outline)
- [ ] **TC-8.3:** Enter or Space key opens file picker from Upload Photo button
- [ ] **TC-8.4:** After photo selection, Tab moves to Submit button
- [ ] **TC-8.5:** Enter key submits the form
- [ ] **TC-8.6:** Tab order is logical (top to bottom)

### 9. Accessibility - Screen Reader

- [ ] **TC-9.1:** Status messages are announced via `aria-live="polite"`
- [ ] **TC-9.2:** Upload button has proper label association
- [ ] **TC-9.3:** Form elements are properly labeled
- [ ] **TC-9.4:** Focus moves to status message when displayed

### 10. Accessibility - Color Contrast

- [ ] **TC-10.1:** Run Chrome DevTools Lighthouse accessibility audit
- [ ] **TC-10.2:** Color contrast ratio is at least 4.5:1 for all text
- [ ] **TC-10.3:** Accessibility score is 90+ in Lighthouse

### 11. Mobile Device Testing - iOS Safari

**Device:** [Device name, iOS version]

- [ ] **TC-11.1:** Page loads correctly on iOS Safari
- [ ] **TC-11.2:** Native iOS photo picker opens
- [ ] **TC-11.3:** Can select photo from camera roll
- [ ] **TC-11.4:** Thumbnail preview displays correctly
- [ ] **TC-11.5:** Touch targets are easily tappable (44x44px minimum)
- [ ] **TC-11.6:** Upload completes successfully
- [ ] **TC-11.7:** Success message displays correctly
- [ ] **TC-11.8:** No console errors in Safari developer tools
- [ ] **TC-11.9:** Page loads within 3 seconds on local network

### 12. Mobile Device Testing - Android Chrome

**Device:** [Device name, Android version]

- [ ] **TC-12.1:** Page loads correctly on Android Chrome
- [ ] **TC-12.2:** Native Android photo picker opens
- [ ] **TC-12.3:** Can select photo from gallery
- [ ] **TC-12.4:** Thumbnail preview displays correctly
- [ ] **TC-12.5:** Touch targets are easily tappable (44x44px minimum)
- [ ] **TC-12.6:** Upload completes successfully
- [ ] **TC-12.7:** Success message displays correctly
- [ ] **TC-12.8:** No console errors in Chrome DevTools
- [ ] **TC-12.9:** Page loads within 3 seconds on local network

### 13. Production Environment Testing

**URL:** `http://10.0.17.1/` or `http://photoshare.local/`

- [ ] **TC-13.1:** Page accessible at production URL
- [ ] **TC-13.2:** Full upload flow works in production environment
- [ ] **TC-13.3:** Mobile devices can connect and upload photos
- [ ] **TC-13.4:** DNS resolution works if configured (`photoshare.local`)

---

## Test Results Summary

**Date:** _______________
**Tester:** _______________
**Total Tests:** 70+
**Passed:** _______________
**Failed:** _______________
**Blocked:** _______________

---

## Issues Found

| Test Case | Issue Description | Severity | Status |
|-----------|------------------|----------|--------|
| TC-X.X | [Description] | High/Medium/Low | Open/Fixed |

---

## Notes

[Add any additional observations, browser-specific quirks, or recommendations here]

---

## Sign-off

- [ ] All critical test cases passed
- [ ] No blocking issues remain
- [ ] Story ready for production deployment

**Tester Signature:** _______________
**Date:** _______________
