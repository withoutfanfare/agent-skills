# Alpine patterns

Worked examples for the patterns named in SKILL.md. Each one is complete
enough to copy and adapt; none of them is the finished component you ship,
because your project's spacing, colours and class names will differ.

## Dropdown menu

Closes on an outside click or Escape, and reports its open state to
assistive technology.

```html
<div x-data="{ open: false }" class="relative">
    <button
        @click="open = !open"
        @keydown.escape.window="open = false"
        :aria-expanded="open"
        aria-haspopup="true"
        type="button"
    >
        Account
    </button>

    <div
        x-show="open"
        x-cloak
        @click.outside="open = false"
        x-transition:enter="motion-safe:transition motion-safe:duration-100"
        x-transition:enter-start="motion-safe:opacity-0 motion-safe:scale-95"
        x-transition:enter-end="motion-safe:opacity-100 motion-safe:scale-100"
        role="menu"
        class="absolute mt-2"
    >
        <a href="/orders" role="menuitem">Orders</a>
        <a href="/settings" role="menuitem">Settings</a>
    </div>
</div>
```

## Modal with a focus trap

A modal needs its own `role`, must trap Tab inside itself while open, and
must give focus back to whatever opened it.

```html
<div x-data="{ open: false }">
    <button @click="open = true" type="button">Edit address</button>

    <div
        x-show="open"
        x-cloak
        x-trap.noscroll="open"
        @keydown.escape.window="open = false"
        role="dialog"
        aria-modal="true"
        aria-labelledby="address-modal-title"
        class="fixed inset-0 flex items-center justify-center"
    >
        <div @click.outside="open = false" class="rounded-lg bg-white p-6">
            <h2 id="address-modal-title">Edit delivery address</h2>
            <!-- form fields -->
            <button @click="open = false" type="button">Save</button>
            <button @click="open = false" type="button">Cancel</button>
        </div>
    </div>
</div>
```

`x-trap` is the official Alpine focus plugin; without it, trap focus by
hand with a `keydown.tab` handler that cycles between the modal's first and
last focusable elements.

## Tabs with arrow key navigation

```html
<div x-data="{ active: 'sizing' }">
    <div role="tablist" @keydown.arrow-right.prevent="$focus.next()" @keydown.arrow-left.prevent="$focus.previous()">
        <button
            role="tab"
            :aria-selected="active === 'sizing'"
            :tabindex="active === 'sizing' ? 0 : -1"
            @click="active = 'sizing'"
        >
            Sizing
        </button>
        <button
            role="tab"
            :aria-selected="active === 'shipping'"
            :tabindex="active === 'shipping' ? 0 : -1"
            @click="active = 'shipping'"
        >
            Shipping
        </button>
    </div>

    <div role="tabpanel" x-show="active === 'sizing'">Sizing details go here.</div>
    <div role="tabpanel" x-show="active === 'shipping'">Shipping details go here.</div>
</div>
```

`$focus.next()`/`$focus.previous()` need the official Focus plugin; without
it, move focus by hand with `$refs` and `.focus()`.

## Accordion, several items open at once

```html
<div x-data="{ open: [] }">
    <template x-for="item in ['returns', 'warranty', 'care']" :key="item">
        <div>
            <button
                @click="open.includes(item) ? open = open.filter(i => i !== item) : open.push(item)"
                :aria-expanded="open.includes(item)"
            >
                <span x-text="item"></span>
            </button>
            <div x-show="open.includes(item)" x-collapse></div>
        </div>
    </template>
</div>
```

`x-collapse` is the official Collapse plugin and gives a smooth height
animation for free; without it, use `x-transition` on opacity only, since
animating `height: auto` needs extra work.

## Shared state with a store

Use a store when two or more components that do not share a parent need
the same value, for example a basket icon in the header and a basket panel
elsewhere on the page.

```js
// stores/basket.js
document.addEventListener('alpine:init', () => {
    Alpine.store('basket', {
        items: [],

        get count() {
            return this.items.reduce((total, item) => total + item.quantity, 0);
        },

        add(product) {
            const existing = this.items.find((item) => item.id === product.id);

            if (existing) {
                existing.quantity++;
            } else {
                this.items.push({ ...product, quantity: 1 });
            }

            this.$dispatch('basket:changed');
        },
    });
});
```

```html
<span x-data x-text="$store.basket.count"></span>
```

## Binding to a backend component's state

Frameworks that render server-side components with a live wire back to the
server (Livewire is the common example) offer a helper that keeps an Alpine
value in step with a server property, usually called something like
`@entangle('propertyName')`. Use it only for values the server genuinely
needs to know about; for anything purely visual (an open flag, a hover
state) keep it in local `x-data` instead, since round-tripping every
keystroke to the server for a value the server never reads adds latency for
no benefit.

```html
<div x-data="{ quantity: @entangle('quantity') }">
    <button @click="quantity++" type="button">+</button>
    <span x-text="quantity"></span>
    <button @click="quantity--" type="button">-</button>
</div>
```

Call a server-side method from Alpine with the framework's own call helper
(for example `$wire.call('save')`), and show a loading state while it
resolves:

```html
<div x-data="{ saving: false }">
    <button
        @click="saving = true; $wire.call('save').then(() => saving = false)"
        :disabled="saving"
        type="button"
    >
        <span x-show="!saving">Save</span>
        <span x-show="saving">Saving…</span>
    </button>
</div>
```
