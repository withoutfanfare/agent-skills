# Filament patterns and field reference

## A resource's shape

Filament 4 generates the form and table into their own classes
(`Schemas/SubscriptionForm.php`, `Tables/SubscriptionsTable.php`); they are
inline here so the whole shape fits on one screen.

```php
declare(strict_types=1);

namespace App\Filament\Resources\Subscriptions;

use App\Filament\Resources\Subscriptions\Pages;
use App\Models\Subscription;
use BackedEnum;
use Filament\Actions\ActionGroup;
use Filament\Actions\BulkActionGroup;
use Filament\Actions\DeleteBulkAction;
use Filament\Actions\EditAction;
use Filament\Actions\ViewAction;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Resources\Resource;
use Filament\Schemas\Components\Section;
use Filament\Schemas\Schema;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Filters\SelectFilter;
use Filament\Tables\Table;
use Illuminate\Support\Str;
use UnitEnum;

class SubscriptionResource extends Resource
{
    protected static ?string $model = Subscription::class;
    protected static string | BackedEnum | null $navigationIcon = 'heroicon-o-credit-card';
    protected static string | UnitEnum | null $navigationGroup = 'Billing';

    public static function form(Schema $schema): Schema
    {
        return $schema->components([
            Section::make('Plan')->schema([
                Select::make('customer_id')
                    ->relationship('customer', 'email')
                    ->searchable()
                    ->required(),
                TextInput::make('plan_name')
                    ->required()
                    ->maxLength(120)
                    ->live(onBlur: true)
                    ->afterStateUpdated(fn ($state, $set) => $set('reference', Str::upper(Str::slug($state, '_')))),
                TextInput::make('reference')
                    ->required()
                    ->unique(ignoreRecord: true),
            ])->columns(2)->columnSpanFull(),
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table
            ->defaultSort('created_at', 'desc')
            ->columns([
                TextColumn::make('plan_name')->searchable()->sortable(),
                TextColumn::make('customer.email')->sortable(),
            ])
            ->filters([
                SelectFilter::make('status')->options([
                    'active' => 'Active',
                    'paused' => 'Paused',
                ]),
            ])
            ->recordActions([
                ActionGroup::make([
                    ViewAction::make(),
                    EditAction::make(),
                ]),
            ])
            ->toolbarActions([
                BulkActionGroup::make([
                    DeleteBulkAction::make(),
                ]),
            ]);
    }

    public static function getPages(): array
    {
        // Route names map 1:1 to the page classes generated alongside this resource.
        return [
            'index' => Pages\ListSubscriptions::route('/'),
            'create' => Pages\CreateSubscription::route('/create'),
            'edit' => Pages\EditSubscription::route('/{record}/edit'),
        ];
    }
}
```

Bulk actions work either way: listed directly they show as separate
buttons, and wrapped in `BulkActionGroup::make()` they sit behind one
dropdown. Pick one per panel and stay consistent.

## Form components at a glance

- Text: `TextInput`, `Textarea`, `RichEditor`, `MarkdownEditor`
- Choice: `Select`, `Radio`, `CheckboxList`, `Toggle`
- Other: `FileUpload`, `DateTimePicker`, `Repeater`, `KeyValue`

## Table columns at a glance

- Display: `TextColumn` (add `->badge()` for a status pill; the old
  `BadgeColumn` is deprecated), `IconColumn`, `ImageColumn`
- Interactive: `ToggleColumn` (inline toggle), `TextInputColumn` (inline
  edit)

## A custom action

```php
use Filament\Actions\Action;

Action::make('pause')
    ->action(fn (Subscription $record) => $record->pause())
    ->requiresConfirmation()
    ->color('warning')
    ->icon('heroicon-o-pause')
    ->visible(fn (Subscription $record) => $record->status === 'active');
```

## A stats widget

```php
use Filament\Widgets\StatsOverviewWidget as BaseWidget;
use Filament\Widgets\StatsOverviewWidget\Stat;

class SubscriptionStats extends BaseWidget
{
    protected function getStats(): array
    {
        return [
            Stat::make('Active subscriptions', Subscription::active()->count()),
            Stat::make('Paused', Subscription::paused()->count()),
            Stat::make('Monthly recurring revenue', Subscription::active()->sum('monthly_price')),
        ];
    }
}
```

## Global search

```php
// Global search also needs a title attribute on the resource.
protected static ?string $recordTitleAttribute = 'plan_name';

public static function getGloballySearchableAttributes(): array
{
    return ['plan_name', 'customer.email'];
}
```

## Soft deletes and relation managers

```php
use Filament\Actions\ForceDeleteAction;
use Filament\Actions\RestoreAction;
use Filament\Tables\Filters\TrashedFilter;

->filters([TrashedFilter::make()])
->recordActions([
    RestoreAction::make(),
    ForceDeleteAction::make(),
])
```

```php
use App\Filament\Resources\Subscriptions\RelationManagers;

public static function getRelations(): array
{
    return [RelationManagers\InvoicesRelationManager::class];
}
```

## Authorisation test pair

```php
it('lets a billing manager reach the resource', function () {
    $manager = User::factory()->billingManager()->create();

    $this->actingAs($manager)
        ->get(SubscriptionResource::getUrl('index'))
        ->assertSuccessful();
});

it('refuses a user without the billing role', function () {
    $shopper = User::factory()->create();

    $this->actingAs($shopper)
        ->get(SubscriptionResource::getUrl('index'))
        ->assertForbidden();
});
```

## Gotchas beyond the SKILL.md steps

- `->default()` only applies on the create page; it is ignored on edit and
  never backfills an existing record. Use a database default or a model
  attribute default instead.
- `FileUpload` writes to the `public` disk unless told otherwise, so an
  uploaded receipt or logo 404s until `php artisan storage:link` has run on
  the target environment.
- `->unique()` without `ignoreRecord: true` fails validation against the
  record's own row every time someone edits it.
