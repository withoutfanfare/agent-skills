# Audit briefs

One brief per area. Fill in the placeholders from the orient step, and add
or remove items to fit the stack and business. Every brief ends with the
same contract.

**Contract for every audit:** return a structured list. For each item:
what exists (file and line), what is missing, a severity (*blocker*,
*major* or *minor*) and a timing: *before launch*, *soon after launch* or
*later*. Read code only; do not run the application. Facts, not prose.

---

## Technical and operations

You are auditing <stack> at <path>, which <one-line description>. Check:

1. **Backups:** what is backed up, how often, where to, and whether a
   restore has ever been tested. Is the one thing that cannot be recreated
   (uploaded files, a particular database) included?
2. **Errors and alerts:** where exceptions go; whether anyone is
   notified; whether the alert destination is configured.
3. **Scheduled work:** every scheduled task and queue worker; what happens
   if one stops; whether anything notices.
4. **Failed jobs:** retry limits, where permanent failures go, whether
   anyone is told.
5. **Deployment:** steps, manual steps, migrations, the way back.
6. **Configuration:** required settings, defaults that are unsafe in
   production, secrets handling.
7. **Health:** a health check exists and covers the database, queue and
   critical outside services.
8. **Capacity:** unbounded queries or uploads, missing timeouts, rate
   limits.

## Money path

You are auditing the ordering and payment code of <stack> at <path>. The
business sells <what> through <payment provider>, fulfilled by <how>.
Check:

1. **Payment events:** which provider events are handled; which obvious
   ones are not (failed payment, dispute, refund, expired checkout).
2. **Failed fulfilment:** when fulfilment fails for good, who is told, and
   is the order marked?
3. **Refunds and cancellations:** the flow, the status changes, the
   customer message.
4. **Tax:** calculated where, and for which regions.
5. **Stale items:** can someone pay for something removed or changed
   during checkout? Is it re-checked at payment?
6. **Customer emails:** which exist and which are sent:
   confirmation, dispatch, failure, refund.
7. **Order visibility:** can customers see their order's status?
8. **Recovery:** abandoned checkout follow-up, if any, and whether it is
   scheduled.
9. **Fraud checks:** what exists, and whether it is called from the order
   flow (search for where it is used, not only where it is defined).

## Being found (public sites)

You are auditing the public website of <stack> at <path>. Check:

1. **Sitemaps:** exist, cover every content type, update on publish.
2. **Analytics:** installed; meaningful events sent (sign-up, purchase),
   not only page views; consent handled.
3. **Languages:** if several, real translations or one language behind
   translated addresses; `hreflang` correct.
4. **Structured data:** product, article, breadcrumb and organisation
   markup where relevant; review markup tied to real reviews.
5. **Page metadata:** titles, descriptions and share images per page;
   duplicate pages marked as such.
6. **Email sign-up:** captured, and connected to something that sends.
7. **Product feeds:** exist and are valid for their destination, if the
   business sells through them.
