# Laravel implementation detail

Applies the method in `SKILL.md` to a Laravel codebase.

## Versioned routes

Give each version its own prefix and route file, and keep its controllers
in their own namespace (`App\Http\Controllers\Api\V1`), imported by class
in that version's file, so a v2 controller never accidentally serves a v1
route. On Laravel 11 and later, run `php artisan install:api` first: new apps
ship without `routes/api.php` or Sanctum.

```php
// routes/api.php
Route::prefix('v1')->name('v1.')->group(base_path('routes/api_v1.php'));
Route::prefix('v2')->name('v2.')->group(base_path('routes/api_v2.php'));
```

A deprecated version's controller stays in place and keeps working; add
middleware that stamps the response with `Deprecation` and `Sunset`
headers rather than deleting anything before the published date:

```php
class DeprecatedVersionHeaders
{
    public function handle(Request $request, Closure $next): Response
    {
        $response = $next($request);
        $response->headers->set('Deprecation', '@1767225600'); // date deprecated, as a Unix timestamp
        $response->headers->set('Sunset', 'Fri, 01 Jan 2027 00:00:00 GMT');
        return $response;
    }
}
```

## Validation with form requests

Keep validation out of the controller, in a form request per action, so the
rules are reusable and testable on their own:

```php
class StoreOrderRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'customer_id' => ['required', 'exists:customers,id'],
            'items' => ['required', 'array', 'min:1'],
            'items.*.sku' => ['required', 'string'],
            'items.*.quantity' => ['required', 'integer', 'min:1'],
        ];
    }
}
```

## Shaping responses with API resources

An API resource controls exactly what goes over the wire, independent of
the model's columns, and is the place to add conditional fields and
relationship links:

```php
class OrderResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'status' => $this->status,
            'total' => $this->total,
            'placed_at' => $this->created_at->toIso8601String(),
            'customer' => $this->whenLoaded('customer', fn () => [
                'id' => $this->customer->id,
                'name' => $this->customer->name,
            ]),
        ];
    }
}
```

Returning `OrderResource::collection($query->paginate())` from the
controller already produces the `data`/`links`/`meta` pagination shape from
step 4 of `SKILL.md`, so prefer `paginate()` over `get()` on any collection
endpoint that could grow.

## Mapping exceptions to the error envelope

Centralise the mapping in one place, so every endpoint's errors go through
the same conversion instead of each controller building its own JSON. On
Laravel 11 and later there is no `App\Exceptions\Handler`; register a
render callback in `bootstrap/app.php`. Returning `null` hands the
exception back to Laravel's default rendering:

```php
->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (Throwable $e, Request $request) {
        if (! $request->expectsJson()) {
            return null;
        }

        return match (true) {
            $e instanceof ValidationException => response()->json([
                'error' => [
                    'code' => 'VALIDATION_FAILED',
                    'message' => 'The request could not be processed.',
                    'details' => collect($e->errors())->map(
                        fn ($messages, $field) => ['field' => $field, 'message' => $messages[0]]
                    )->values(),
                ],
            ], 422),
            $e instanceof AuthenticationException => response()->json([
                'error' => ['code' => 'UNAUTHENTICATED', 'message' => 'Authentication required.'],
            ], 401),
            $e instanceof AccessDeniedHttpException => response()->json([
                'error' => ['code' => 'FORBIDDEN', 'message' => 'You cannot perform this action.'],
            ], 403),
            $e instanceof NotFoundHttpException => response()->json([
                'error' => ['code' => 'NOT_FOUND', 'message' => 'The resource was not found.'],
            ], 404),
            default => null,
        };
    });
})
```

By the time a render callback runs, Laravel has already turned an
`AuthorizationException` into `AccessDeniedHttpException` and a
`ModelNotFoundException` into `NotFoundHttpException`, which is why the
callback matches the Symfony classes. On Laravel 10 and older, override
`render()` in `app/Exceptions/Handler.php` instead: that method sees the
original `AuthorizationException` and `ModelNotFoundException`, so match
those, and fall back to `parent::render($request, $e)` instead of `null`.

## Authentication

Sanctum's token abilities give a single scheme for both first-party and
third-party API clients: issue a personal access token with named
abilities, and check them per route rather than building a parallel
permission system.

The `ability` and `abilities` middleware are not registered by default;
alias them in `bootstrap/app.php` first:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias([
        'abilities' => \Laravel\Sanctum\Http\Middleware\CheckAbilities::class,
        'ability' => \Laravel\Sanctum\Http\Middleware\CheckForAnyAbility::class,
    ]);
})
```

```php
$token = $user->createToken('mobile-app', ['orders:read', 'orders:write']);

Route::middleware(['auth:sanctum', 'ability:orders:write'])
    ->post('/v1/orders', [OrderController::class, 'store']);
```
