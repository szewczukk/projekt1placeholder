import { getApiBaseUrl } from "$lib/api/config";

export async function trackProductPageOpen(
	userId: number,
	productId: number,
	fetchFn: typeof fetch = fetch,
): Promise<void> {
	const response = await fetchFn(`${getApiBaseUrl()}/analytics/product-page/open`, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ user_id: userId, product_id: productId }),
	});
	if (!response.ok) {
		return;
	}
}

export async function trackProductPageLeave(
	userId: number,
	productId: number,
	fetchFn: typeof fetch = fetch,
): Promise<void> {
	const response = await fetchFn(`${getApiBaseUrl()}/analytics/product-page/leave`, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ user_id: userId, product_id: productId }),
	});
	if (!response.ok) {
		return;
	}
}
