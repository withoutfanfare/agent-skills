// A minimal Alpine store: state shared between components that do not
// share a parent, such as a basket icon and a basket panel elsewhere on
// the page. Register it before Alpine starts.
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

            // A store is a plain object with no $dispatch, so fire the event on
            // window; listeners use @basket:changed.window.
            window.dispatchEvent(new CustomEvent('basket:changed'));
        },

        remove(productId) {
            this.items = this.items.filter((item) => item.id !== productId);
        },
    });
});
