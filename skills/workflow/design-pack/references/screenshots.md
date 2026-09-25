# Choosing and checking screenshots

## Which routes

Pick 8 to 12 routes between desktop and mobile so that, taken together,
they hit every distinct layout the product uses: a landing or promo page,
a browse or index page, a single-item page, a form, and a signed-in view
if you can reach one without borrowing real credentials. Two screenshots
of the same layout add nothing the tool didn't already learn from the
first.

## Desktop and mobile runs

The script's default filename prefix is empty, so give each run its own
prefix to get the `desktop-*.jpg` and `mobile-*.jpg` names the pack
expects:

```bash
npx -p playwright node "${CLAUDE_SKILL_DIR:-.}/scripts/capture-pages.mjs" \
  --base https://example.test --out design-pack/screenshots --prefix desktop- \
  --routes / /catalogue /product/example /account /contact

npx -p playwright node "${CLAUDE_SKILL_DIR:-.}/scripts/capture-pages.mjs" \
  --base https://example.test --out design-pack/screenshots --prefix mobile- \
  --width 390 --routes / /product/example /contact
```

Two or three mobile captures are enough.

## No real data

Never capture a page holding real customer data, order details or anything
personally identifiable. Use a seeded demo account or a page with sample
content instead, and check each screenshot before it goes in the pack.

## Check the results

Look at a handful of the results before moving on. A capture that stitches
several scrollable slices together can come back looking plausible and
still be wrong: a repeated band at a seam, a section that never finished
animating in, a page that stops short of its own footer. Check the bottom
of a tall page, not just the top.
