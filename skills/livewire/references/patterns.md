# Livewire patterns and worked examples

## Form Object

```php
declare(strict_types=1);

namespace App\Livewire\Forms;

use App\Models\Post;
use Livewire\Attributes\Validate;
use Livewire\Form;

class PostForm extends Form
{
    #[Validate('required|string|max:255')]
    public string $title = '';

    #[Validate('required|string')]
    public string $body = '';

    public function store(): Post
    {
        $this->validate();

        return Post::create($this->only(['title', 'body']));
    }
}
```

```php
class CreatePost extends Component
{
    public PostForm $form;

    public function save(): void
    {
        $post = $this->form->store();
        $this->redirectRoute('posts.show', $post);
    }
}
```

## Data table with URL-bound state

```php
use App\Models\Post;
use Livewire\Attributes\Computed;
use Livewire\Attributes\Url;
use Livewire\Component;
use Livewire\WithPagination;

class PostsTable extends Component
{
    use WithPagination;

    #[Url]
    public string $search = '';

    #[Url]
    public string $sort = 'created_at';

    // The URL is user input: only these columns may be sorted on.
    private const SORTABLE = ['created_at', 'title'];

    public function updatingSearch(): void
    {
        $this->resetPage();
    }

    #[Computed]
    public function posts()
    {
        return Post::query()
            ->when($this->search, fn ($q) => $q->where('title', 'like', "%{$this->search}%"))
            ->orderBy(in_array($this->sort, self::SORTABLE, true) ? $this->sort : 'created_at')
            ->paginate(20);
    }
}
```

## Modal opened from elsewhere

```php
// Anywhere in the app
$this->dispatch('open-confirm-modal', postId: $post->id);

// The modal component
#[On('open-confirm-modal')]
public function open(int $postId): void
{
    $this->postId = $postId;
    $this->show = true;
}

public function close(): void
{
    $this->reset(['show', 'postId']);
    $this->resetValidation();
}
```

## File upload with preview

```php
class AvatarUpload extends Component
{
    use WithFileUploads;

    public $photo;

    public function updatedPhoto(): void
    {
        $this->validate(['photo' => 'image|max:2048']);
    }
}
```

```blade
<input type="file" wire:model="photo">
<div wire:loading wire:target="photo">Uploading...</div>
@if ($photo)
    <img src="{{ $photo->temporaryUrl() }}">
@endif
```

## Nested components in a loop

```blade
@foreach ($items as $item)
    <livewire:item-row :item="$item" :key="$item->id" />
@endforeach
```

Children dispatch events upward; parents listen with `#[On]` rather than
reaching into a child's state directly.

## Computed property caching

`#[Computed]` caches for the whole request. Reading it again after
mutating the data it depends on returns the stale value unless you clear
it:

```php
// Livewire resolves the Post from the ID the browser sends, like route
// model binding. That ID is user input, so authorise before acting.
public function delete(Post $post): void
{
    Gate::authorize('delete', $post); // use Illuminate\Support\Facades\Gate;
    $post->delete();
    unset($this->posts); // force the next read to recompute
}
```

## Alpine interop

```blade
<div x-data="{ open: $wire.entangle('showPanel') }">
    <button @click="open = ! open">Toggle</button>
</div>
```

The `@entangle` Blade directive is deprecated; use `$wire.entangle()`, or
read `$wire.showPanel` directly. `$wire.call('method')` calls a Livewire
method from Alpine;
`@event-name.window="handler"` listens for a dispatched event anywhere on
the page.

## SPA navigation and persistence

`wire:navigate` on a link swaps the page without a full reload.
`@persist('name') ... @endpersist` keeps a DOM subtree (an audio player, an
open dropdown) alive across those navigations instead of remounting it.

## Testing validation explicitly

```php
Livewire::test(CreatePost::class)
    ->set('form.title', '')
    ->call('save')
    ->assertHasErrors(['form.title' => 'required']);
```
