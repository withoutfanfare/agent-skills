# Standard journeys

Use as a checklist when building the scenario list, then add what is
specific to the product.

## Every site

- Home page loads without console errors or failed requests.
- Main navigation reaches every top-level page; no dead links.
- Search returns sensible results, and "no results" is handled.
- Forms: success, each validation error, and a server error.
- Phone-width viewport: navigation, forms and tables usable.
- Page titles and descriptions present and specific.
- 404 page is helpful.

## Accounts

- Sign up, including a duplicate email.
- Email verification link, including an expired one.
- Sign in, wrong password, account lockout or throttling.
- Password reset from start to finish.
- Sign out, then the back button does not show private pages.
- Profile update, including email change.
- Access to another user's records by changing the ID in the address.

## Shops

- Browse, filter, sort, and view a product.
- Add to basket, change quantity, remove, empty basket.
- Discount codes: valid, expired, invalid.
- Checkout with test payment: success, declined card, abandoned payment.
- Order confirmation page and email; order in the account.
- Item removed or out of stock during checkout.
- Totals, tax and delivery correct at every step.

## Subscription products

- Start a trial or plan; upgrade; downgrade; cancel; resume.
- Failed renewal payment and what the user sees.
- Limits enforced on each plan.
- Invoices downloadable and correct.

## Admin areas

- Only admins can reach any admin page.
- Create, edit and delete for each managed item, with confirmation for
  deletes.
- Bulk actions and exports on a realistic number of rows.
- Changes appear on the public site as expected.
