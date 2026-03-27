import { getApiBaseUrl } from "$lib/api/config";

export type CheckoutLineItem = {
	product_id: number;
	name: string;
	quantity: number;
	unit_price: number;
	subtotal: number;
};

export type CheckoutResponse = {
	order_id: number;
	user_id: number;
	items: CheckoutLineItem[];
	total: number;
	message: string;
};

export type ApiErrorBody = {
	detail?: string | { msg?: string }[];
};

export async function parseApiErrorMessage(response: Response): Promise<string> {
	let text = "";
	try {
		const body: unknown = await response.clone().json();
		if (
			body &&
			typeof body === "object" &&
			"detail" in body &&
			typeof (body as ApiErrorBody).detail === "string"
		) {
			return (body as ApiErrorBody).detail as string;
		}
	} catch {
		try {
			text = await response.text();
		} catch {
			/* ignore */
		}
	}
	if (text) {
		return text;
	}
	return `Żądanie nie powiodło się (${response.status})`;
}

async function jsonOrThrow(response: Response): Promise<void> {
	if (response.ok) {
		return;
	}
	const message = await parseApiErrorMessage(response);
	throw new Error(message);
}

export async function apiAddToCart(
	userId: number,
	productId: number,
	quantity: number,
	fetchFn: typeof fetch = fetch,
): Promise<void> {
	const response = await fetchFn(`${getApiBaseUrl()}/cart/add`, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({
			user_id: userId,
			product_id: productId,
			quantity,
		}),
	});
	await jsonOrThrow(response);
}

export async function apiRemoveFromCart(
	userId: number,
	productId: number,
	fetchFn: typeof fetch = fetch,
): Promise<void> {
	const response = await fetchFn(`${getApiBaseUrl()}/cart/remove`, {
		method: "DELETE",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({
			user_id: userId,
			product_id: productId,
		}),
	});
	await jsonOrThrow(response);
}

export async function apiCheckout(
	userId: number,
	fetchFn: typeof fetch = fetch,
): Promise<CheckoutResponse> {
	const response = await fetchFn(`${getApiBaseUrl()}/cart/checkout`, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ user_id: userId }),
	});
	if (!response.ok) {
		const message = await parseApiErrorMessage(response);
		throw new Error(message);
	}
	return response.json() as Promise<CheckoutResponse>;
}
