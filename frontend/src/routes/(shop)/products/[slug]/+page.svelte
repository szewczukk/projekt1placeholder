<script lang="ts">
	import ProductHeroImage from "$lib/components/product-detail/ProductHeroImage.svelte";
	import ProductNotFound from "$lib/components/product-detail/ProductNotFound.svelte";
	import ProductPurchaseCard from "$lib/components/product-detail/ProductPurchaseCard.svelte";
	import type { PageData } from "./$types";

	let { data }: { data: PageData } = $props();
	const product = $derived(data.product);
	let quantity = $state(1);

	const incrementQuantity = () => {
		quantity += 1;
	};

	const decrementQuantity = () => {
		quantity = Math.max(1, quantity - 1);
	};

	const handleAddToCart = () => {
		if (!product) {
			return;
		}

		// TODO: replace with real cart store/service integration.
		console.log("Mock add to cart", {
			productId: product.id,
			productName: product.name,
			quantity,
		});
	};
</script>

<svelte:head>
	<title>{product ? `${product.name} | Sklep` : "Produkt nie znaleziony | Sklep"}</title>
</svelte:head>

{#if product}
	<section class="min-h-screen bg-gradient-to-br from-slate-50 via-zinc-100 to-slate-200 p-6 md:p-10">
		<div class="mx-auto flex w-full max-w-7xl justify-between">
			<a
				href="/"
				class="rounded-full border border-slate-300/80 bg-white/80 px-4 py-2 text-sm font-medium text-slate-700 backdrop-blur transition hover:bg-white"
			>
				Powrót do listy
			</a>
			<a
				href="/checkout"
				class="rounded-full bg-slate-900 px-5 py-2 text-sm font-semibold text-white shadow-lg shadow-slate-900/20 transition hover:-translate-y-0.5 hover:bg-black"
			>
				Koszyk
			</a>
		</div>

		<div class="mx-auto mt-6 grid min-h-[calc(100vh-9rem)] w-full max-w-7xl items-center gap-8 lg:grid-cols-[1.2fr_1fr]">
			<ProductHeroImage name={product.name} imageUrl={`https://picsum.photos/seed/product-${product.id}/1200/1200`} />
			<ProductPurchaseCard
				{product}
				{quantity}
				onIncrement={incrementQuantity}
				onDecrement={decrementQuantity}
				onAddToCart={handleAddToCart}
			/>
		</div>
	</section>
{:else}
	<ProductNotFound />
{/if}
