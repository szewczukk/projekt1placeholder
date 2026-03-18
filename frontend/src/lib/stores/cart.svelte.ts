import type { Product } from "$lib/api/products";

export type CartItem = {
	product: Product;
	quantity: number;
};

class CartState {
	private _items = $state<Record<number, CartItem>>({});

	get items(): CartItem[] {
		return Object.values(this._items);
	}

	get totalItems(): number {
		return this.items.reduce((sum, item) => sum + item.quantity, 0);
	}

	get totalPrice(): number {
		return this.items.reduce((sum, item) => sum + item.product.price * item.quantity, 0);
	}

	get isEmpty(): boolean {
		return this.totalItems === 0;
	}

	getItem(productId: number): CartItem | undefined {
		return this._items[productId];
	}

	addItem(product: Product, quantity: number): void {
		const existing = this._items[product.id];
		if (existing) {
			this._items[product.id] = { ...existing, quantity: existing.quantity + quantity };
		} else {
			this._items[product.id] = { product, quantity };
		}
		// TODO: POST /cart/items { productId: product.id, quantity }
	}

	updateQuantity(productId: number, quantity: number): void {
		if (quantity <= 0) {
			this.removeItem(productId);
			return;
		}
		const item = this._items[productId];
		if (item) {
			this._items[productId] = { ...item, quantity };
			// TODO: POST /cart/items { productId, quantity }
		}
	}

	removeItem(productId: number): void {
		const { [productId]: _, ...rest } = this._items;
		this._items = rest;
		// TODO: DELETE /cart/items/{productId}
	}

	checkout(): void {
		// TODO: POST /cart/checkout
		this._items = {};
	}

	clear(): void {
		this._items = {};
	}
}

// TODO: GET /cart — sync cart state from backend on app init
export const cart = new CartState();
