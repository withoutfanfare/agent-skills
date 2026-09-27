# Laravel notes

Worked examples for the strategies in the main skill, using a subscription
app where each tenant is a company with its own workspace.

## Shared tables with a tenant column

Give tenant-owned tables a `tenant_id` foreign key, indexed, and apply a
global scope through a trait so every model that uses it is scoped without
repeating the logic:

```php
trait BelongsToTenant
{
    protected static function bootBelongsToTenant(): void
    {
        static::addGlobalScope('tenant', function (Builder $query) {
            $tenant = app()->bound('currentTenant') ? app('currentTenant') : null;

            if ($tenant) {
                $query->where($query->qualifyColumn('tenant_id'), $tenant->id);
            } else {
                $query->whereRaw('1 = 0'); // no tenant: no rows, never every tenant's rows
            }
        });

        static::creating(function (Model $model) {
            $tenant = app()->bound('currentTenant') ? app('currentTenant') : null;

            if ($tenant) {
                // A tenant is bound: always stamp its id, never trust one the
                // caller (a controller, a mass-assigned request) already set.
                $model->tenant_id = $tenant->id;
            } elseif (! isset($model->tenant_id)) {
                throw new LogicException('No current tenant for a tenant-owned record.');
            }
        });
    }
}
```

Asking the container for `currentTenant` when nothing is bound throws, and
a scope that skips itself when there is no tenant fails open, which is why
the trait checks `bound()` and returns no rows instead. Bind `currentTenant`
once, in middleware, and every model using the trait picks it up
automatically. Run that middleware before route model binding
(`SubstituteBindings`), or bound models are looked up before the tenant is
known:

```php
class ResolveTenant
{
    public function handle(Request $request, Closure $next)
    {
        $subdomain = explode('.', $request->getHost())[0];
        $tenant = Tenant::where('slug', $subdomain)->first();

        abort_unless($tenant, 404);
        abort_if($request->user() && $request->user()->tenant_id !== $tenant->id, 403);

        app()->instance('currentTenant', $tenant);

        return $next($request);
    }
}
```

`SubstituteBindings` comes from the `web` group and sits in Laravel's
middleware priority list, which reorders a route's middleware; a
`resolve.tenant` added to the route is not in that list, so a
route-model-bound parameter (`Route::put('/invoices/{invoice}', ...)`) can
resolve before the tenant is known. Put `ResolveTenant` ahead of
`SubstituteBindings` in the priority list:

```php
// bootstrap/app.php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->prependToPriorityList(
        before: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        prepend: \App\Http\Middleware\ResolveTenant::class,
    );
})
```

Reach across tenants deliberately with `withoutGlobalScope('tenant')`, kept
to admin controllers and named so it is easy to find later:

```php
Invoice::withoutGlobalScope('tenant')->where('status', 'overdue')->get();
```

Composite indexes should lead with the tenant column, since almost every
query filters on it first:

```php
$table->index(['tenant_id', 'status']);
```

## Separate database per tenant

Configure a connection with the database left blank, then set it and
reconnect once the tenant is known:

```php
// config/database.php
'tenant' => [
    'driver' => 'mysql',
    'database' => '',
    // host, username, password as usual
],
```

```php
class TenantConnection
{
    public function switchTo(Tenant $tenant): void
    {
        config(['database.connections.tenant.database' => $tenant->database_name]);
        DB::purge('tenant');
        DB::reconnect('tenant');
    }
}
```

Give tenant-scoped models a base class pinned to that connection, so a
model can never accidentally query the wrong tenant's database:

```php
abstract class TenantModel extends Model
{
    protected $connection = 'tenant';
}
```

Run this switch on every request in middleware, the same as tenant
resolution for the shared-table approach, and purge the connection at the
end of the request so a pooled worker never carries one tenant's database
into the next request it handles.

## Queue jobs

A queued job never inherits the container binding a request middleware set
up, but `php artisan queue:work` is a long-running daemon that keeps one
booted application in memory and works through many jobs in that same
process, so a binding set by one job is still there when the next job
starts unless something clears it. Pass the tenant into the job's
constructor, rebind it at the start of `handle()`, and clear it again once
the job finishes so the next job on the same worker never inherits it:

```php
class GenerateInvoice implements ShouldQueue
{
    public function __construct(public Tenant $tenant, public int $subscriptionId) {}

    public function handle(): void
    {
        app()->instance('currentTenant', $this->tenant);

        try {
            $subscription = Subscription::findOrFail($this->subscriptionId);
            // proceeds scoped to $this->tenant
        } finally {
            app()->forgetInstance('currentTenant');
        }
    }
}
```

For separate-database tenancy, also call the connection switch at the top
of `handle()` before the job touches any tenant model, and purge that
connection in the same `finally` block so a pooled worker never carries one
tenant's database into the next job it picks up.

## Testing isolation

```php
it('only lists the current tenant records', function () {
    $tenantA = Tenant::factory()->create();
    $tenantB = Tenant::factory()->create();

    app()->instance('currentTenant', $tenantA);
    $ownInvoice = Invoice::factory()->create();

    app()->instance('currentTenant', $tenantB);
    Invoice::factory()->create();

    app()->instance('currentTenant', $tenantA);

    expect(Invoice::all())->toHaveCount(1)
        ->and(Invoice::first()->is($ownInvoice))->toBeTrue();
});

it('refuses to update another tenants record', function () {
    $tenantA = Tenant::factory()->create(['slug' => 'acme']);
    $tenantB = Tenant::factory()->create();
    $user = User::factory()->create(['tenant_id' => $tenantA->id]);
    $foreignInvoice = Invoice::factory()->create(['tenant_id' => $tenantB->id, 'status' => 'draft']);

    $this->actingAs($user)
        ->put("http://acme.example.test/invoices/{$foreignInvoice->id}", ['status' => 'paid'])
        ->assertNotFound();

    expect($foreignInvoice->fresh()->status)->toBe('draft');
});

it('allows the owner to update their own record', function () {
    $tenantA = Tenant::factory()->create(['slug' => 'acme']);
    $user = User::factory()->create(['tenant_id' => $tenantA->id]);

    app()->instance('currentTenant', $tenantA);
    $ownInvoice = Invoice::factory()->create(['status' => 'draft']);

    $this->actingAs($user)
        ->put("http://acme.example.test/invoices/{$ownInvoice->id}", ['status' => 'paid'])
        ->assertOk();

    expect($ownInvoice->fresh()->status)->toBe('paid');
});
```

Without the priority-list fix above, this test fails even for the owner's
own record: `SubstituteBindings` looks up `{invoice}` while the tenant
scope still sees no bound tenant, so the global scope adds `1 = 0` and the
model never resolves, a 404 the owner has no way to fix.

## Keeping admin routes out of tenant scope

```php
Route::middleware(['auth', 'resolve.tenant'])->group(function () {
    Route::get('/dashboard', DashboardController::class);
});

Route::middleware(['auth', 'can:operate-platform'])->prefix('operator')->group(function () {
    Route::get('/tenants', TenantIndexController::class);
});
```

The operator group never runs `resolve.tenant`, so it can list and manage
every tenant; the dashboard group always resolves one, so it never can.

## Packages worth knowing

A few established packages cover most of this for you rather than hand
rolling it: `stancl/tenancy` (full single- or multi-database tenancy with
tenant-aware queues and storage), `spatie/laravel-multitenancy` (a lighter
shared or separate-database approach). Reach for one of these before
building the connection-switching machinery from scratch, unless the
project's needs are simple enough that the trait-and-middleware approach
above is the whole job.
