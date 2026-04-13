<script lang="ts">
import type { Product } from "$lib/api/products";
import QuantitySelector from "./QuantitySelector.svelte";

type Props = {
	product: Product;
	quantity: number;
	onIncrement: () => void;
	onDecrement: () => void;
	onAddToCart: () => void | Promise<void>;
	addToCartError?: string | null;
	maxSelectableInBatch: number;
};

let {
	product,
	quantity,
	onIncrement,
	onDecrement,
	onAddToCart,
	addToCartError = null,
	maxSelectableInBatch,
}: Props = $props();
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
		{#if addToCartError}
			<p class="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-800 ring-1 ring-red-200">
				{addToCartError}
			</p>
		{/if}
		{#if maxSelectableInBatch <= 0}
			<p class="rounded-xl bg-amber-50 px-4 py-3 text-sm text-amber-900 ring-1 ring-amber-200">
				{#if product.quantity <= 0}
					Brak towaru na magazynie.
				{:else}
					Masz już w koszyku cały dostępny stan ({product.quantity} szt.).
				{/if}
			</p>
		{/if}
		<QuantitySelector
			{quantity}
			{onIncrement}
			{onDecrement}
			disableDecrement={quantity <= 1 || maxSelectableInBatch <= 0}
			disableIncrement={quantity >= maxSelectableInBatch || maxSelectableInBatch <= 0}
		/>
		<button
			type="button"
			class="inline-flex items-center justify-center rounded-2xl bg-slate-900 px-6 py-4 text-lg font-semibold text-white shadow-lg shadow-slate-900/30 transition hover:-translate-y-0.5 hover:bg-black cursor-pointer disabled:cursor-not-allowed disabled:opacity-50"
			onclick={onAddToCart}
			disabled={maxSelectableInBatch <= 0}
		>
			Dodaj do koszyka
		</button>
	</div>
</article>
