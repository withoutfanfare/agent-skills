---
name: mailroom
description: >-
  Builds a Laravel mailable and its Markdown template so a transactional
  email renders correctly in real inboxes, queues instead of blocking the
  request, and always has a plain fallback link. Use when creating a
  mailable, running make:mail, building a transactional or notification
  email, or the user asks for an order confirmation, welcome email or
  similar. Not for choosing channels or sending SMS, chat or push alerts;
  use `notify`.
license: MIT
allowed-tools: Read Write Edit Grep Glob Bash
---

# Mailroom

An email that looks right in the browser preview can still arrive broken:
a missing plain-text fallback, a button that renders as a blank box in
Outlook, or a mailable that blocks the HTTP request while it talks to the
mail server. None of that shows up until a real recipient reports it. This
skill builds the mailable so the common failures are ruled out before the
first send.

To pick channels or fire one event across email, SMS, chat or push, use
`notify` (if installed).

## 1. Scaffold with the right structure

```bash
php artisan make:mail OrderConfirmation --markdown=emails.orders.confirmation
```

Markdown mail is the default choice: it gives a consistent, tested layout
and produces the plain-text version automatically. Reach for a plain Blade
view only when the design cannot fit the Markdown components at all, and
if you do, write the plain-text alternative by hand rather than leaving it
out.

Done when: the mailable class and its Markdown view both exist and the
class implements `ShouldQueue`.

## 2. Write the envelope and content deliberately

`envelope()` sets the subject, from address and any reply-to; `content()`
points at the Markdown view and the data it needs. Pass a resource or an
array of primitive values into the view, not a whole Eloquent model with
relations still lazy, so the render never triggers a query for a
relationship nobody loaded.

```php
public function envelope(): Envelope
{
    return new Envelope(subject: "Your order #{$this->order->reference} is confirmed");
}

public function content(): Content
{
    return new Content(
        markdown: 'emails.orders.confirmation',
        with: ['order' => $this->order->loadMissing('lineItems')],
    );
}
```

A subject line that states the outcome ("Your order is confirmed") beats a
generic one ("Order update"); it is what the recipient sees before opening
anything.

Done when: the subject names the specific outcome, and every relation the
view touches was eager-loaded before the mailable was built.

## 3. Build the template from the mail components

Use the built-in components rather than hand-rolled HTML: they are already
tested against the inconsistent CSS support of real mail clients.

```blade
<x-mail::message>
# Order confirmed

Thanks, {{ $order->customer_name }}. Here's what you ordered:

<x-mail::table>
| Item | Qty | Price |
|:-----|:---:|------:|
@foreach ($order->lineItems as $line)
| {{ $line->name }} | {{ $line->quantity }} | {{ $line->formatted_price }} |
@endforeach
</x-mail::table>

<x-mail::button :url="$order->tracking_url">
Track your order
</x-mail::button>

<x-mail::subcopy>
If the button above doesn't work, copy this link into your browser:
{{ $order->tracking_url }}
</x-mail::subcopy>
</x-mail::message>
```

Every button needs a `subcopy` fallback with the plain URL underneath it:
some clients strip the button's link entirely and this is the only way
those recipients can still act on the email. Keep the layout to a single
column under 600px; anything wider gets clipped or forces horizontal
scrolling in the clients that still render at a fixed width.

Done when: every `<x-mail::button>` has a matching `<x-mail::subcopy>`
fallback link directly under it.

## 4. Queue it, and prove the failure path is handled

```php
Mail::to($order->customer_email)->queue(new OrderConfirmation($order));
```

Sending synchronously (`send()` instead of `queue()`) ties the mail
server's response time to the request the user is waiting on; a slow or
down mail server then makes an unrelated action feel broken. Queue by
default, and reserve `send()` for something that genuinely must be
confirmed sent before the response returns (rare).

If the mailable can fail to build (a missing attachment, absent data),
that failure needs somewhere to go: a queue failure listener, a `failed()`
callback, or monitoring on the failed-jobs table. A silently dropped
confirmation email is invisible until the customer asks where it went.

Done when: sending goes through `queue()`, and there is a defined answer
for what happens if the queued job fails.

## 5. Preview and test before the first real send

Add a preview route that returns the mailable so you can see the rendered
HTML in a browser, and register it only inside an
`app()->environment('local')` check so it can never reach production. Then
write a test with `Mail::fake()` and `Mail::assertQueued()`.

`Mail::fake()` proves the mailable was dispatched to the right recipient
without touching a real mail server. Instantiate the mailable directly in
a second assertion to check its rendered subject and that key content
(the order reference, the tracking link) actually appears in the body;
"was sent" and "says the right thing" are different claims and both need
covering.

Done when: a fake-backed test asserts both the recipient and the rendered
content, and you have looked at the rendered HTML in the preview route at
least once.

The guarded preview route and the Pest test patterns, worked through:
[references/testing.md](references/testing.md).

## It's working if

- Every button in the email has a working plain-link fallback beneath it.
- Sending an email never blocks the request that triggered it.
- A test fails if the wrong recipient or the wrong content goes into the
  email, not just if the mailable throws.
