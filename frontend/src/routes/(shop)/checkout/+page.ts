import { getProducts } from "$lib/api/products";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch }) => {
  const products = await getProducts(fetch);
  return { products };
};
