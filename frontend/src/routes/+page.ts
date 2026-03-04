import { getProducts } from "$lib/api/products";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch }) => {
	return {
		products: await getProducts(fetch),
	};
};
