import { getProducts } from "$lib/api/products";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, params }) => {
	const products = await getProducts(fetch);
	const product = products.find((item) => String(item.id) === params.slug) ?? null;

	return { product };
};
