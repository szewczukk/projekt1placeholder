<script lang="ts">
import type { Product } from "$lib/api/products";
import CartLink from "$lib/components/CartLink.svelte";
import type { PageData } from "./$types";

let { data }: { data: PageData } = $props();
const products = $derived(data.products as Product[]);
</script>

<svelte:head>
	<title>Produkty | Sklep</title>
</svelte:head>

<section
	class="min-h-screen bg-gradient-to-br from-slate-50 via-zinc-100 to-slate-200 p-6 md:p-10"
>
	<div class="mx-auto flex w-full max-w-7xl justify-end">
		<CartLink />
	</div>

	<div class="mx-auto mt-6 w-full max-w-7xl">
		<h1 class="text-3xl font-black text-slate-900 md:text-4xl">Produkty</h1>
		<p class="mt-2 text-slate-600">
			{products.length === 0
				? "Brak produktów."
				: `${products.length} ${products.length === 1 ? "produkt" : "produktów"} w sklepie.`}
		</p>

		{#if products.length > 0}
			<ul class="mt-8 flex flex-wrap gap-4">
				{#each products as product (product.id)}
					<li class="min-w-0 flex-[1_1_16rem]">
						<a
							href={`/products/${product.id}`}
							class="group flex h-[22rem] flex-col overflow-hidden rounded-2xl bg-white shadow-xl ring-1 ring-slate-200 transition hover:shadow-slate-900/10 hover:ring-slate-300"
						>
							<div class="h-64 shrink-0 w-full overflow-hidden bg-slate-100">
								<img
									src={`https://picsum.photos/seed/product-${product.id}/256/256`}
									alt={product.name}
									class="h-full w-full object-cover transition duration-300 group-hover:scale-105"
								/>
							</div>
							<div class="flex min-h-0 flex-1 flex-col gap-1 p-4">
								<div class="flex items-baseline justify-between gap-2">
									<h2 class="text-lg font-bold text-slate-900 group-hover:text-slate-700">
										{product.name}
									</h2>
									<p class="shrink-0 text-xl font-black tracking-tight text-slate-900">
										{product.price.toFixed(2)} zl
									</p>
								</div>
							</div>
						</a>
					</li>
				{/each}
			</ul>
		{:else}
			<div
				class="mt-12 rounded-3xl bg-white/80 p-12 text-center shadow-xl ring-1 ring-slate-200/80 backdrop-blur"
			>
				<p class="text-slate-600">Brak produktów w sklepie.</p>
			</div>
		{/if}
	</div>
</section>
