import { apiAddToCart, apiCheckout, apiRemoveFromCart, type CheckoutResponse } from "$lib/api/cart";
import type { Product } from "$lib/api/products";
import { ensureSession, getUserId } from "$lib/session";

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

	async addItem(product: Product, quantity: number): Promise<void> {
		if (quantity <= 0) {
			return;
		}
		await ensureSession();
		const userId = getUserId();
		const existing = this._items[product.id];
		const previous: CartItem | undefined = existing ? { ...existing } : undefined;
		if (existing) {
			this._items[product.id] = { ...existing, quantity: existing.quantity + quantity };
		} else {
			this._items[product.id] = { product, quantity };
		}
		try {
			await apiAddToCart(userId, product.id, quantity);
		} catch (e) {
			if (previous) {
				this._items[product.id] = previous;
			} else {
				const { [product.id]: _, ...rest } = this._items;
				this._items = rest;
			}
			throw e;
		}
	}

	async updateQuantity(productId: number, quantity: number): Promise<void> {
		if (quantity <= 0) {
			await this.removeItem(productId);
			return;
		}
		await ensureSession();
		const userId = getUserId();
		const item = this._items[productId];
		if (!item) {
			return;
		}
		const oldQty = item.quantity;
		if (quantity === oldQty) {
			return;
		}
		if (quantity > oldQty) {
			const delta = quantity - oldQty;
			this._items[productId] = { ...item, quantity };
			try {
				await apiAddToCart(userId, productId, delta);
			} catch (e) {
				this._items[productId] = { ...item, quantity: oldQty };
				throw e;
			}
			return;
		}
		try {
			await apiRemoveFromCart(userId, productId);
			await apiAddToCart(userId, productId, quantity);
			this._items[productId] = { ...item, quantity };
		} catch (e) {
			try {
				await apiAddToCart(userId, productId, oldQty);
			} catch {
				/* best effort restore server cart */
			}
			throw e;
		}
	}

	async removeItem(productId: number): Promise<void> {
		const previous = this._items[productId];
		if (!previous) {
			return;
		}
		await ensureSession();
		const userId = getUserId();
		const { [productId]: _, ...rest } = this._items;
		this._items = rest;
		try {
			await apiRemoveFromCart(userId, productId);
		} catch (e) {
			this._items[productId] = previous;
			throw e;
		}
	}

	async checkout(): Promise<CheckoutResponse> {
		await ensureSession();
		const userId = getUserId();
		const response = await apiCheckout(userId);
		this._items = {};
		return response;
	}

	clear(): void {
		this._items = {};
	}
}

export const cart = new CartState();
