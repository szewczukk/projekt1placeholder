<script lang="ts">
import type { Product } from "$lib/api/products";
import QuantitySelector from "./QuantitySelector.svelte";

type Props = {
	product: Product;
	quantity: number;
	onIncrement: () => void;
	onDecrement: () => void;
	onAddToCart: () => void;
};

let { product, quantity, onIncrement, onDecrement, onAddToCart }: Props = $props();
</script>

<article class="rounded-3xl bg-white p-8 shadow-2xl ring-1 ring-slate-200 md:p-10">
	<p
		class="mb-3 inline-flex rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold text-emerald-700"
	>
		Dostępne: {product.quantity} szt.
	</p>
	<h1 class="text-3xl font-black text-slate-900 md:text-5xl">{product.name}</h1>
	<p class="mt-6 text-base leading-relaxed text-slate-600 md:text-lg">{product.description}</p>
	<p class="mt-8 text-4xl font-black tracking-tight text-slate-900">
		{product.price.toFixed(2)}
		zl
	</p>

	<div class="mt-8 flex flex-col gap-4">
		<QuantitySelector {quantity} {onIncrement} {onDecrement} />
		<button
			type="button"
			class="inline-flex items-center justify-center rounded-2xl bg-slate-900 px-6 py-4 text-lg font-semibold text-white shadow-lg shadow-slate-900/30 transition hover:-translate-y-0.5 hover:bg-black cursor-pointer"
			onclick={onAddToCart}
		>
			Dodaj do koszyka
		</button>
	</div>
</article>
