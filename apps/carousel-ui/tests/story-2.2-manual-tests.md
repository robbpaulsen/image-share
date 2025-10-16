# Story 2.2 Manual Test Checklist

## Test Environment Setup
- [ ] Backend server running
- [ ] Carousel UI accessible
- [ ] Browser DevTools console open for debugging

---

## Part 1: Dynamic Photo Detection (AC 1-7)

### AC 1-3: Polling Mechanism
- [ ] Open browser console
- [ ] Verify initial fetch occurs on page load
- [ ] Confirm polling starts with 10-second interval
- [ ] Check console logs show "Starting photo polling (10000ms interval)"
- [ ] Wait 10 seconds and verify another fetch occurs
- [ ] Confirm fetch requests go to `/api/photos`

### AC 4-5: Dynamic Photo Addition
- [ ] Start with carousel displaying photos
- [ ] Upload a new photo via upload UI
- [ ] Within 10 seconds, verify new photo appears in carousel
- [ ] Check that photos are in chronological order (oldest to newest)
- [ ] Upload multiple photos and verify all appear

### AC 6: Transition from No Photos State
- [ ] Delete all photos from `display_images/` directory
- [ ] Wait for polling cycle to detect empty state
- [ ] Verify instruction screen is displayed
- [ ] Upload one photo
- [ ] Within 10 seconds, verify automatic transition to carousel
- [ ] Confirm photo displays correctly

### AC 7: Console Logging
- [ ] Upload 1 photo while monitoring console
- [ ] Verify log shows: "Detected 1 new photos: [filename]"
- [ ] Upload 3 more photos
- [ ] Verify log shows: "Detected 3 new photos: [filenames]"

---

## Part 2: No Photos State (AC 8-13)

### AC 8-9: Instruction Screen Content
- [ ] Clear all photos from `display_images/` directory
- [ ] Refresh carousel page
- [ ] Verify instruction screen displays:
  - [ ] Heading: "Share Your Event Photos!"
  - [ ] Wi-Fi info: "Connect to: ImageShare-Demo"
  - [ ] Upload URL: "Open: http://photoshare.local or http://10.0.17.1"
  - [ ] QR code visible and properly formatted

### AC 10: QR Code Functionality
- [ ] Open smartphone camera app
- [ ] Point camera at QR code on screen
- [ ] Verify camera recognizes QR code
- [ ] Confirm decoded URL is `http://photoshare.local`
- [ ] Test QR code scan from 3-5 feet away

### AC 11: Readability from Distance
- [ ] Stand 10 feet from display
- [ ] Verify heading text is clearly readable
- [ ] Confirm Wi-Fi network name is readable
- [ ] Confirm URL is readable
- [ ] Check high contrast between text and background

### AC 12: Smooth Transition to Carousel
- [ ] Start with empty `display_images/` directory
- [ ] Verify instruction screen displays
- [ ] Upload first photo
- [ ] Within 10 seconds, observe transition
- [ ] Verify crossfade effect (1 second duration)
- [ ] Confirm instruction screen opacity goes to 0
- [ ] Confirm carousel opacity goes to 1
- [ ] Verify photo displays correctly after transition

### AC 13: Revert to No Photos State
- [ ] Start with carousel showing 3+ photos
- [ ] Delete all photos from `display_images/`
- [ ] Wait for next polling cycle (within 10 seconds)
- [ ] Verify carousel transitions back to instruction screen
- [ ] Confirm instruction screen displays correctly
- [ ] Verify console shows: "All photos deleted, returning to instruction screen"

---

## Additional Edge Cases

### Single Photo Behavior
- [ ] Clear all photos
- [ ] Upload exactly 1 photo
- [ ] Verify photo displays (no rotation)
- [ ] Upload second photo
- [ ] Verify rotation starts

### Rapid Photo Uploads
- [ ] Upload 5 photos in quick succession (< 10 seconds)
- [ ] Verify all photos detected on next polling cycle
- [ ] Confirm console shows correct count

### Network Interruption
- [ ] Disconnect network during polling
- [ ] Verify console shows error (but app doesn't crash)
- [ ] Reconnect network
- [ ] Verify polling resumes

### Browser Refresh
- [ ] Refresh page while carousel is running
- [ ] Verify polling resumes after refresh
- [ ] Confirm QR code regenerates correctly

---

## Test Results

**Date:**
**Tester:**
**Result:** ☐ PASS ☐ FAIL
**Notes:**
