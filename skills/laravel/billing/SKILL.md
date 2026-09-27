---
name: billing
description: >-
  Adds subscription or one-off billing with Laravel Cashier (Stripe): the
  Billable model, Checkout, subscription lifecycle including trials, SCA
  and cancellation, webhooks as the source of truth, invoices, the
  customer portal, and proving the whole flow in Stripe test mode. Use
  when the user asks to add subscriptions, take payments, integrate
  Stripe or Cashier, or handle a Stripe webhook. Not for general API
  design (use `api-design`) or notifications (use `notify`).
license: MIT
allowed-tools: Read Grep Glob Bash Edit Write
---

# Billing

A subscription flow that renders a checkout page proves nothing about
whether the subscription record updates when Stripe reports a payment
failed three days later. Stripe's webhooks are the actual source of truth
for a subscription's state; anything that only listens to the redirect at
the end of Checkout will drift the moment a card is declined or a
customer cancels from Stripe's own portal. This skill wires the whole
loop, in test mode, before any of it touches real money.

**Hard guardrails.** Never put a live (`sk_live_...`, `pk_live_...`) key
in code, a log line, or a chat message. Never execute a real charge,
refund or payout while doing this work; stay in Stripe test mode
throughout. If the user wants to go live, that switch is theirs to make.

## 1. Set up the Billable model

```bash
composer require laravel/cashier
php artisan vendor:publish --tag="cashier-migrations"
php artisan migrate
```

Add `use Laravel\Cashier\Billable;` to the billable model, and use
Stripe's test keys (`sk_test_...`, `pk_test_...`) plus a test
`STRIPE_WEBHOOK_SECRET` in `.env` for all of this work.

Done when: the model uses `Billable` and the Cashier tables exist.

## 2. Define products and prices in Stripe, not in application code

Create products and their prices in the Stripe dashboard (test mode), and
reference them by their `price_...` ID. Do not hardcode an amount in PHP
that Stripe is meant to be the source of truth for; a price changed in
the dashboard should not need a deploy to take effect.

Done when: every price used in code is a Stripe price ID, not a raw
number.

## 3. Choose Checkout or Elements

Stripe Checkout, via `$user->checkout([...])` or
`$user->newSubscription(...)->checkout()`, redirects to a Stripe-hosted
page and needs no card handling in your own code; it is the right default
for most projects. Elements embeds Stripe's own fields in your page and
needs a `SetupIntent` for a subscription or a `PaymentMethod` for a single
charge. Only reach for Elements when the checkout page genuinely must not
leave the site.

Done when: the choice is written down, not defaulted to Elements out of
habit.

## 4. Build the subscription and its trial

```php
$user->newSubscription('default', 'price_monthly')
    ->trialDays(10)
    ->create($paymentMethodId);
```

A trial with no payment method up front is a separate case
(`$user->trial_ends_at`), not a shorter version of the same call; decide
which one the product needs before writing the trial length anywhere.

Done when: `onTrial()` reflects the intended trial length on a real test
subscription.

## 5. Handle incomplete and past_due states (SCA)

A card needing Strong Customer Authentication leaves the subscription
`incomplete` until the customer confirms it. Check
`$user->hasIncompletePayment('default')` and send them to
`route('cashier.payment', $subscription->latestPayment()->id)` to finish
authenticating, rather than treating the subscription as failed. Decide
separately whether a `past_due` subscription keeps access
(`Cashier::keepPastDueSubscriptionsActive()`) or loses it immediately,
which is the default.

Done when: an incomplete payment sends the customer to finish
authentication, and the past_due behaviour is a deliberate choice.

## 6. Make the webhook the source of truth

Cashier registers `/stripe/webhook` for you. Exclude it from CSRF
verification (it is not a browser form submission):

```php
->withMiddleware(fn (Middleware $middleware) =>
    $middleware->validateCsrfTokens(except: ['stripe/*'])
)
```

Set `STRIPE_WEBHOOK_SECRET` so Cashier verifies each request actually
came from Stripe; a webhook route with no secret configured accepts
anything sent to that URL. Handle events beyond Cashier's defaults by
listening for `Laravel\Cashier\Events\WebhookReceived`, or by extending
Cashier's controller, rather than polling Stripe from your own code. Stripe
retries a webhook it did not get a 200 for, so treat every handler as if
it might run twice: check the event has not already been processed
(Stripe sends an event ID) before applying its effect again.

Done when: the CSRF exclusion, the webhook secret, and idempotent
handling are all in place, not just the route existing.

## 7. Manage subscription changes deliberately

```php
$user->subscription('default')->swap('price_yearly');   // prorates
$user->subscription('default')->noProrate()->swap('price_yearly');
$user->subscription('default')->cancel();                // ends at period end
$user->subscription('default')->cancelNow();
$user->subscription('default')->resume();                // only within grace period
```

A cancelled subscription stays `onGracePeriod()` until the period ends;
decide what access looks like during that window, since "cancelled" and
"access already revoked" are not the same moment.

Done when: swap, cancel and resume have each been exercised against a
real test subscription, not just read from the docs.

## 8. Invoices, the customer portal, and tax

`$user->invoices()` and `$user->redirectToBillingPortal(route('dashboard'))`
cover invoice history and self-service billing without building those
screens yourself. For tax, `Cashier::calculateTaxes()` in
`AppServiceProvider::boot()` turns on Stripe Tax for new subscriptions and
invoices, provided the customer's billing address and any tax ID are
synced to Stripe; without that call, Cashier does not calculate tax.

Done when: the portal link works for a test customer, and the tax
decision is stated, not silent.

## 9. Prove the flow end to end in test mode

```bash
stripe listen --forward-to localhost:8000/stripe/webhook
stripe trigger customer.subscription.created
```

`stripe listen` prints its own signing secret (`whsec_...`); put that in
the local `STRIPE_WEBHOOK_SECRET`, or every forwarded event fails signature
checks. Run `stripe listen` locally so webhooks reach the app, use a Stripe test
card (`4242 4242 4242 4242`, any future expiry, any CVC) to complete a
real Checkout session, and `stripe trigger` to fire the events the
handler expects. Confirm the local subscription record changed as a
result, not only that Stripe's dashboard shows the event delivered.

Done when: a test-mode Checkout completion and a triggered webhook have
both been observed to update the application's own data.

## 10. Report

State the billing model (subscription, one-off, or both), Checkout or
Elements and why, the webhook events handled and how idempotency is
enforced, the cancel and grace period behaviour, and the step 9 evidence
that a test-mode run updated real application data.

Done when: the report quotes the step 9 command output, not a
description of what should happen.

## It's working if

- No live key or real charge appears anywhere in the work, only test
  mode throughout.
- The webhook route is CSRF-exempt, signature-verified, and idempotent
  against a retried event, not just handling the happy path once.
- A test-mode Checkout completion and a `stripe trigger` event have both
  been shown to change the application's own subscription data.
