# Carousel UI Manual Testing Checklist

## Story 2.1: Carousel Display with Automatic Rotation

**Test Date:** _________
**Tested By:** _________
**Test Environment:** _________

---

## Pre-requisites

- [ ] Server is running (`cd apps/api && uv run uvicorn main:app --host 0.0.0.0 --port 8000`)
- [ ] Test images are available in `/image-share-data/display_images/`
- [ ] Physical HDMI display is connected (for AC15)

---

## Test Cases

### Part 1: Basic Display (AC 1-9)

#### AC1: HTML carousel page accessible
- [ ] Navigate to `http://10.0.17.1/display` (or `http://localhost:8000/display`)
- [ ] Page loads without errors
- [ ] No 404 or 500 errors in browser console

#### AC2: Full-screen view with no browser chrome
- [ ] Press F11 to enter fullscreen/kiosk mode
- [ ] Verify no browser UI elements visible
- [ ] Image fills available space

#### AC3: Page loads images from display_images directory
- [ ] Check browser Network tab for `/api/photos` request
- [ ] Verify request succeeds (200 status)
- [ ] Confirm response contains photo array

#### AC4: API returns JSON sorted chronologically
- [ ] Open `/api/photos` in browser
- [ ] Verify JSON array is returned
- [ ] Check `createdAt` timestamps are in ascending order (oldest first)
- [ ] Verify each photo has `id`, `url`, `createdAt` fields

#### AC5: Photos displayed one at a time, centered and scaled
- [ ] Only one photo visible at a time
- [ ] Photo is centered on screen
- [ ] Photo maintains aspect ratio (no stretching)

#### AC6: Layout handles portrait and landscape
- [ ] Test with portrait image - verify it's centered and scaled correctly
- [ ] Test with landscape image - verify it's centered and scaled correctly
- [ ] Test with square image - verify it's centered and scaled correctly

#### AC7: Black background fills empty space
- [ ] Verify background is pure black (#000000)
- [ ] Check empty space around photos (especially portrait photos)
- [ ] No white or colored borders visible

#### AC8: Initial photo is first in chronological list
- [ ] First photo displayed matches first item in `/api/photos` response
- [ ] Compare filename in browser to API response

#### AC9: CSS uses object-fit: contain
- [ ] Open browser DevTools (F12)
- [ ] Inspect `.carousel-image` element
- [ ] Verify `object-fit: contain` is applied
- [ ] Verify images are not cropped or distorted

---

### Part 2: Automatic Rotation (AC 10-15)

#### AC10: Carousel advances after 7 seconds
- [ ] Start stopwatch when first photo appears
- [ ] Verify transition starts at ~7 seconds
- [ ] Repeat for 3-5 transitions to confirm consistency
- [ ] Average timing: _______ seconds (should be ~7s)

#### AC11: Carousel loops back to first photo
- [ ] Count total number of photos in `/api/photos` response: _____
- [ ] Watch carousel until it completes one full cycle
- [ ] Verify it returns to first photo after last photo
- [ ] Verify looping continues indefinitely (watch 2-3 full cycles)

#### AC12: 1-second crossfade transition
- [ ] Observe transition between photos
- [ ] Verify it's a smooth fade (not an abrupt switch)
- [ ] Time the transition duration (should be ~1 second)
- [ ] Check for any visual glitches during transition

#### AC13: Single photo case - no transitions
- [ ] Clear `display_images/` directory
- [ ] Copy only ONE image to `display_images/`
- [ ] Reload page
- [ ] Verify single photo remains displayed continuously
- [ ] Verify no transitions occur
- [ ] Leave running for 1 minute to confirm stability

#### AC14: No memory leaks for 6+ hours
**Note:** For MVP testing, run for at least 30 minutes

- [ ] Open browser DevTools > Performance Monitor
- [ ] Record initial memory usage: _______ MB
- [ ] Let carousel run for 30 minutes minimum (6 hours for production)
- [ ] Record memory usage every 10 minutes:
  - 10 min: _______ MB
  - 20 min: _______ MB
  - 30 min: _______ MB
  - 1 hour: _______ MB (optional)
  - 2 hours: _______ MB (optional)
- [ ] Verify memory usage stays relatively stable (no continuous growth)
- [ ] Check browser console for any errors or warnings

#### AC15: Validation on physical HDMI display
- [ ] Connect laptop/server to HDMI display
- [ ] Navigate to `http://10.0.17.1/display` from browser
- [ ] Enable fullscreen/kiosk mode (F11)
- [ ] Verify all above acceptance criteria on the physical display
- [ ] Check photo quality and clarity
- [ ] Verify colors and contrast are acceptable
- [ ] Test display resolution: _________
- [ ] No flickering or tearing during transitions

---

## Edge Cases

### No Photos Available
- [ ] Clear all images from `display_images/`
- [ ] Reload page
- [ ] Verify friendly "No photos available" message appears
- [ ] Verify no JavaScript errors in console

### Network Error Handling
- [ ] Stop the backend server while page is loaded
- [ ] Reload page
- [ ] Verify error message appears
- [ ] Restart server and verify page recovers after refresh

### Mixed Image Formats
- [ ] Add images of different formats (.jpg, .png, .heic) to `display_images/`
- [ ] Verify all formats display correctly
- [ ] Check for any format-specific issues

---

## Browser Compatibility

Test on the following browsers:

- [ ] Chrome/Edge (Chromium): Version _________
- [ ] Firefox: Version _________
- [ ] Safari (if available): Version _________

---

## Performance Notes

### Load Times
- Initial page load: _______ seconds
- First photo display: _______ seconds
- Time to fetch photos from API: _______ seconds

### Observed Issues
_List any bugs, glitches, or unexpected behavior:_

1.
2.
3.

---

## Sign-off

- [ ] All acceptance criteria (AC 1-15) have been tested and verified
- [ ] No blocking issues identified
- [ ] Performance is acceptable for production use
- [ ] Ready for deployment

**Tester Signature:** _____________________
**Date:** _____________________
