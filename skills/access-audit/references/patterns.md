# Accessibility patterns

Worked fixes for the issues that come up most often, grouped by the area
they belong to in the main skill.

## Structure and content

Alt text should describe what the image communicates, not that it's an
image. A purely decorative image gets an empty `alt=""` so screen readers
skip it rather than reading a filename.

```html
<!-- Tells the reader nothing -->
<img src="uptake.png">

<!-- Says what the chart shows -->
<img src="uptake.png" alt="Sign-ups grew from 400 to 1,100 over Q3">

<!-- Purely decorative: skip it -->
<img src="divider.png" alt="">
```

Headings should form a single nested outline for the whole page, `h1` down
to whatever depth is needed, without skipping a level to get a smaller
font (use CSS for that instead). Landmark elements (`<nav>`, `<main>`,
`<header>`, `<footer>`) let a screen reader user jump straight to a section
instead of reading everything in between.

A link should read sensibly out of context, because screen reader users
often browse a page's links as a list: "read more" repeated ten times is
useless, "read more about the Q3 results" is not. Reserve `<a>` for
navigation and `<button>` for anything that performs an action in place,
since assistive technology announces the two differently and users expect
different behaviour from each.

## Forms

Every input needs a programmatic label, not just placeholder text that
disappears once typing starts.

```html
<label for="postcode">Postcode</label>
<input id="postcode" name="postcode" autocomplete="postal-code" required
       aria-describedby="postcode-hint">
<p id="postcode-hint">Used to estimate delivery time</p>
```

When validation fails, the error needs to be linked to its field
(`aria-describedby`, plus `aria-invalid="true"` on the input) and announced
as it appears, not only shown in red text nearby:

```html
<input id="email" aria-invalid="true" aria-describedby="email-error">
<p id="email-error" role="alert">Enter an email address with an @ sign</p>
```

## Custom widgets

A native `<button>`, `<select>` or `<input type="checkbox">` gets keyboard
support and screen reader behaviour for free. A custom-built version of the
same thing has to recreate all of it: the ARIA role, the current state, and
the key handling. Get the role and state right but skip the keyboard
handling, and the widget looks correct to a sighted developer testing with
a mouse while being unusable to someone who isn't.

**Dialog that takes over the page:**

```html
<div role="dialog" aria-modal="true" aria-labelledby="dlg-title">
  <h2 id="dlg-title">Remove item?</h2>
  <button>Cancel</button>
  <button>Remove</button>
</div>
```

Move focus into the dialog when it opens, keep Tab cycling only within it
while it's open, and return focus to whatever opened it when it closes.
Escape should close it.

**Tab set:**

```html
<div role="tablist" aria-label="Account settings">
  <button role="tab" aria-selected="true" aria-controls="panel-profile" id="tab-profile">Profile</button>
  <button role="tab" aria-selected="false" aria-controls="panel-security" id="tab-security" tabindex="-1">Security</button>
</div>
<div role="tabpanel" id="panel-profile" aria-labelledby="tab-profile">…</div>
<div role="tabpanel" id="panel-security" aria-labelledby="tab-security" hidden>…</div>
```

Only the selected tab sits in the normal tab order (`tabindex="0"`); the
rest are reached with the arrow keys once focus is inside the tab list.

**Status and error messages that appear without a reload:**

```html
<!-- Routine update: wait for a pause before reading it out -->
<div role="status" aria-live="polite">Basket updated</div>

<!-- Something needs attention now -->
<div role="alert" aria-live="assertive">Payment failed, try again</div>
```

**A control that's busy:**

```html
<button aria-busy="true" disabled>
  <span aria-hidden="true" class="spinner"></span> Saving…
</button>
```

## Keyboard behaviour

| Key | Expected result |
|---|---|
| Tab / Shift+Tab | Move to the next or previous focusable element, in visual reading order |
| Enter | Activate a button, link or submit a form |
| Space | Activate a button, toggle a checkbox |
| Escape | Close whatever is currently open (dialog, menu, dropdown) |
| Arrow keys | Move within a single composite control (tabs, menu, radio group) |

A focus trap, where Tab moves the user in but nothing moves them back out,
is one of the most disabling bugs there is; treat it as blocking severity
wherever it shows up.

```js
// Confine Tab to a modal's own focusable elements while it's open
const focusable = modal.querySelectorAll(
  'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
);
const first = focusable[0];
const last = focusable[focusable.length - 1];

modal.addEventListener('keydown', (event) => {
  if (event.key !== 'Tab') return;
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
});
```

Never remove the browser's focus outline without putting a replacement in
its place; a page with no visible focus indicator is unusable for anyone
navigating by keyboard.

```css
/* Leaves keyboard users with no way to see where they are */
*:focus { outline: none; }

/* Replace it, don't just remove it */
*:focus-visible {
  outline: 2px solid #1a56db;
  outline-offset: 2px;
}
```

## Colour contrast

| Content | Minimum ratio |
|---|---|
| Text under 24px (or under about 18.5px if bold) | 4.5:1 |
| Large text: 24px and up, or about 18.5px and up if bold | 3:1 |
| Icons, borders and other meaningful UI graphics | 3:1 |

Check contrast against the actual rendered background, not the design
file's flat swatch: text over a photo or a gradient can fail in some
areas and pass in others, so sample the worst point, not the average.
WCAG defines large text as 18pt, or 14pt bold; at 1pt = 1.333px that is
24px and about 18.5px.

## Added in WCAG 2.2 (level AA)

- **2.4.11 Focus Not Obscured (Minimum).** When an element takes keyboard
  focus, it is not entirely hidden by content the site added: a sticky
  header, a cookie banner, a chat widget. Tab through with those showing
  and check the focused element stays at least partly visible; a
  `scroll-padding-top` equal to the sticky header's height usually fixes
  it.
- **2.5.8 Target Size (Minimum).** Pointer targets are at least 24 by 24
  CSS pixels. A smaller target passes if a 24px circle centred on it does
  not overlap another target or its circle, if an equivalent control on
  the page meets the size, if it is a link inside a sentence, if the
  browser sets its size, or if the size is essential.
- **3.3.8 Accessible Authentication (Minimum).** No sign-in step demands a
  memory or puzzle test (typing a password from memory, solving a
  puzzle) unless there is another way through. Letting the browser or a
  password manager fill the fields, allowing paste, and offering a
  passkey or a third-party sign-in all count. Blocking paste into a
  password or one-time code field usually fails it, unless another route
  exists.

## Visually hidden content

Text meant for screen readers only (a skip link's destination label, extra
context on an icon-only button) needs to stay in the accessibility tree
while being invisible on screen; `display: none` and `visibility: hidden`
both remove it from that tree entirely, so use a clipping technique
instead:

```css
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

A "skip to main content" link at the very top of the page, visible only
once it receives focus, saves keyboard users from tabbing through an
entire header on every single page:

```css
/* Hidden like .visually-hidden until the link takes focus. */
.visually-hidden-until-focused:not(:focus) {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

```html
<a href="#main" class="visually-hidden-until-focused">Skip to main content</a>
…
<main id="main" tabindex="-1">…</main>
```
