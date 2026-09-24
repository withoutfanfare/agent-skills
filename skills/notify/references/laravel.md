# Laravel notification notes

## Generating a notification

```bash
php artisan make:notification AppointmentReminder
```

## Shape of a multi-channel class

```php
declare(strict_types=1);

namespace App\Notifications;

use App\Models\Appointment;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Messages\MailMessage;
use Illuminate\Notifications\Notification;

class AppointmentReminder extends Notification implements ShouldQueue
{
    use Queueable;

    public function __construct(
        public Appointment $appointment,
    ) {
    }

    public function via(object $notifiable): array
    {
        $default = ['mail', 'database'];

        return $notifiable->reminder_channels ?? $default;
    }

    public function toMail(object $notifiable): MailMessage
    {
        $when = $this->appointment->starts_at->format('l, g:ia');

        return (new MailMessage)
            ->subject('Your appointment is coming up')
            ->line("You're booked in for {$when}.")
            ->action('View appointment', url("/appointments/{$this->appointment->id}"));
    }

    public function toArray(object $notifiable): array
    {
        return [
            'appointment_id' => $this->appointment->id,
            'message' => "Reminder: appointment at {$this->appointment->starts_at->format('g:ia')}",
        ];
    }
}
```

`via()` returning a per-user preference, rather than a fixed array, is how
a recipient's channel choice gets honoured without branching logic
scattered through the class.

## Sending

```php
$customer->notify(new AppointmentReminder($appointment));
Notification::send($attendees, new AppointmentReminder($appointment));

// no user model to hand: route straight to an address
Notification::route('mail', 'guest@example.com')->notify(new AppointmentReminder($appointment));
```

## Channels at a glance

- **mail**: `toMail()` returning a `MailMessage`, or a full Blade view for
  richer content.
- **database**: `toArray()`, stored in a `notifications` table whose
  migration you generate (see Gotchas); pair with a bell or list in the UI.
- **broadcast**: `toBroadcast()`, delivered over a websocket connection for
  live in-app updates; needs a frontend listener wired to the channel.
- **Slack**: `toSlack()` returning a `SlackMessage`; install
  `laravel/slack-notification-channel` and configure a Slack app's bot
  token in `config/services.php`.
- **SMS (Vonage or similar)**: `toVonage()` (or the equivalent driver
  method); install `laravel/vonage-notification-channel` (or the
  provider's own channel package) and configure its credentials; keep the message
  to one segment where possible, providers charge per segment.
- **Custom channel**: a class with a `send($notifiable, $notification)`
  method, referenced by class name in `via()`, for anything without a
  built-in driver.

## Conditional sending and queue configuration

```php
public function via(object $notifiable): array
{
    return $notifiable->wantsSms() ? ['vonage', 'database'] : ['mail', 'database'];
}

public function shouldSend(object $notifiable, string $channel): bool
{
    return ! $notifiable->hasOptedOutOf($channel);
}

public int $tries = 3;
public array $backoff = [10, 30, 60];

public function viaQueues(): array
{
    return ['mail' => 'emails', 'vonage' => 'sms'];
}
```

## Testing with fakes

```php
Notification::fake();

$customer->notify(new AppointmentReminder($appointment));

Notification::assertSentTo(
    $customer,
    AppointmentReminder::class,
    fn (AppointmentReminder $notification) => $notification->appointment->id === $appointment->id
);
```

`Mail::fake()`, `Queue::fake()`, `Http::fake()` work the same way for
notifications that go through those underlying services directly.

## Gotchas

- Without `ShouldQueue`, a mail or SMS send blocks the request until the
  outside service responds, which turns a slow provider into a slow page.
- The database channel needs its own migration
  (`php artisan make:notifications-table` then `migrate`) before `toArray()`
  notifications will store anywhere.
- A `via()` that always returns every channel regardless of preference
  means an opted-out user still gets texted.
