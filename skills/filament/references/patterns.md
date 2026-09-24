# Filament patterns and field reference

## A resource's shape

```php
declare(strict_types=1);

namespace App\Filament\Resources;

use App\Filament\Resources\SubscriptionResource\Pages;
use App\Models\Subscription;
use Filament\Forms\Components\Section;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables\Actions\ActionGroup;
use Filament\Tables\Actions\DeleteBulkAction;
use Filament\Tables\Actions\EditAction;
use Filament\Tables\Actions\ViewAction;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Filters\SelectFilter;
use Filament\Tables\Table;

class SubscriptionResource extends Resource
{
    protected static ?string $model = Subscription::class;
    protected static ?string $navigationIcon = 'heroicon-o-credit-card';
    protected static ?string $navigationGroup = 'Billing';

    public static function form(Form $form): Form
    {
        return $form->schema([
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
            ])->columns(2),
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
            ->actions([
                ActionGroup::make([
                    ViewAction::make(),
                    EditAction::make(),
                ]),
            ])
            ->bulkActions([
                DeleteBulkAction::make(),
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

## Form components at a glance

- Text: `TextInput`, `Textarea`, `RichEditor`, `MarkdownEditor`
- Choice: `Select`, `Radio`, `CheckboxList`, `Toggle`
- Other: `FileUpload`, `DateTimePicker`, `Repeater`, `KeyValue`

## Table columns at a glance

- Display: `TextColumn`, `BadgeColumn`, `IconColumn`, `ImageColumn`
- Interactive: `ToggleColumn` (inline toggle), `TextInputColumn` (inline
  edit)

## A custom action

```php
Tables\Actions\Action::make('pause')
    ->action(fn (Subscription $record) => $record->pause())
    ->requiresConfirmation()
    ->color('warning')
    ->icon('heroicon-o-pause')
    ->visible(fn (Subscription $record) => $record->status === 'active');
```

## A stats widget

```php
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
public static function getGloballySearchableAttributes(): array
{
    return ['plan_name', 'customer.email'];
}
```

## Soft deletes and relation managers

```php
->filters([Tables\Filters\TrashedFilter::make()])
->actions([
    Tables\Actions\RestoreAction::make(),
    Tables\Actions\ForceDeleteAction::make(),
])
```

```php
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
