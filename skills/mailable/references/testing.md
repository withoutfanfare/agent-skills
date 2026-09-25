# Testing mailables (Pest)

## Asserting a mailable was queued with the right content

```php
it('queues an order confirmation with the tracking link', function () {
    Mail::fake();

    $order = Order::factory()->create();
    Mail::to($order->customer_email)->queue(new OrderConfirmation($order));

    Mail::assertQueued(OrderConfirmation::class, function (OrderConfirmation $mail) use ($order) {
        return $mail->hasTo($order->customer_email)
            && str_contains($mail->render(), $order->reference);
    });
});
```

`hasTo()` checks the envelope; `render()` renders the actual Markdown
template, so a check against its output catches a template that renders
without the data it was supposed to show, which `assertQueued()` alone
would not.

## Asserting nothing was sent when it shouldn't be

```php
it('does not email a cancelled order', function () {
    Mail::fake();

    $order = Order::factory()->cancelled()->create();
    (new NotifyCustomerOfOrderStatus($order))->handle();

    Mail::assertNothingQueued();
});
```

A negative assertion like this catches the class of bug where a condition
that should suppress the email gets removed or inverted later.

## Checking the subject line directly

```php
it('states the order reference in the subject', function () {
    $order = Order::factory()->create(['reference' => 'ABC-123']);
    $mail = new OrderConfirmation($order);

    expect($mail->envelope()->subject)->toContain('ABC-123');
});
```

Building the mailable directly, rather than going through `Mail::fake()`,
is the simplest way to test the envelope in isolation.

## Preview route guard

Keep the preview route (used in step 5 of `SKILL.md`) out of anything that
could reach production:

```php
if (app()->environment('local')) {
    Route::get('/mail-preview/order-confirmation', fn () =>
        new OrderConfirmation(Order::factory()->create())
    );
}
```

The guard runs once, when routes are registered, so a test that switches
the environment afterwards passes whatever the guard does. Check it from
the command line instead; this should report no matching routes:

```bash
APP_ENV=production php artisan route:list --path=mail-preview
```
