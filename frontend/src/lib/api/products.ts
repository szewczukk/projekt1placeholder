import { env } from "$env/dynamic/public";

export type Product = {
	id: number;
	name: string;
	description: string;
	price: number;
	quantity: number;
};

const API_BASE_URL = env.PUBLIC_API_BASE_URL || "http://localhost:8000";

const isProduct = (value: unknown): value is Product => {
	if (!value || typeof value !== "object") {
		return false;
	}

	const candidate = value as Record<string, unknown>;

	return (
		typeof candidate.id === "number" &&
		typeof candidate.name === "string" &&
		typeof candidate.description === "string" &&
		typeof candidate.price === "number" &&
		typeof candidate.quantity === "number"
	);
};

// TODO: Add image field to the product and display it in the UI
export const getProducts = async (fetchFn: typeof fetch): Promise<Product[]> => {
	const response = await fetchFn(`${API_BASE_URL}/products`);

	if (!response.ok) {
		throw new Error(`Nie udało się pobrać produktów (${response.status})`);
	}

	const payload: unknown = await response.json();

	if (!Array.isArray(payload)) {
		return [];
	}

	return payload.filter(isProduct);
};
