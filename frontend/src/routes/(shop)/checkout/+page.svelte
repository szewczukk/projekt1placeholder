<script lang="ts">
import type { CheckoutResponse } from "$lib/api/cart";
import CartItem from "$lib/components/checkout/CartItem.svelte";
import { cart } from "$lib/stores/cart.svelte";

let checkoutLoading = $state(false);
let checkoutError = $state<string | null>(null);
let lastOrder = $state<CheckoutResponse | null>(null);

$effect(() => {
	if (!cart.isEmpty) {
		lastOrder = null;
	}
});

const handleCheckout = async () => {
	checkoutError = null;
	checkoutLoading = true;
	try {
		lastOrder = await cart.checkout();
	} catch (e) {
		lastOrder = null;
		checkoutError =
			e instanceof Error ? e.message : "Nie udało się zrealizować zamówienia.";
	} finally {
		checkoutLoading = false;
	}
};
</script>

<svelte:head>
	<title>Koszyk | Sklep</title>
</svelte:head>

<section
	class="min-h-screen bg-gradient-to-br from-slate-50 via-zinc-100 to-slate-200 p-6 md:p-10"
>
	<div class="mx-auto flex w-full max-w-7xl justify-between">
		<a
			href="/"
			class="rounded-full border border-slate-300/80 bg-white/80 px-4 py-2 text-sm font-medium text-slate-700 backdrop-blur transition hover:bg-white"
		>
			Powrót do listy
		</a>
		<a
			href="/"
			class="rounded-full bg-slate-900 px-5 py-2 text-sm font-semibold text-white shadow-lg shadow-slate-900/20 transition hover:-translate-y-0.5 hover:bg-black"
		>
			Sklep
		</a>
	</div>

	<div class="mx-auto mt-6 w-full max-w-7xl">
		<h1 class="text-3xl font-black text-slate-900 md:text-4xl">Koszyk</h1>
		<p class="mt-2 text-slate-600">
			{#if lastOrder && cart.isEmpty}
				Zamówienie #{lastOrder.order_id} zrealizowane.
			{:else if cart.isEmpty}
				Brak produktów w koszyku.
			{:else}
				{cart.items.length}
				{cart.items.length === 1 ? "produkt" : "produktów"} w koszyku.
			{/if}
		</p>

		{#if lastOrder && cart.isEmpty}
			<div
				class="mt-8 rounded-3xl bg-white p-8 shadow-xl ring-1 ring-slate-200 md:p-10"
			>
				<p class="text-lg font-semibold text-emerald-800">{lastOrder.message}</p>
				<p class="mt-2 text-slate-600">
					Numer zamówienia:
					<span class="font-bold text-slate-900">{lastOrder.order_id}</span>
					· Łącznie:
					<span class="font-bold text-slate-900"
						>{lastOrder.total.toFixed(2)} zl</span
					>
				</p>
				<ul class="mt-6 divide-y divide-slate-100">
					{#each lastOrder.items as line (line.product_id)}
						<li class="flex flex-wrap justify-between gap-2 py-3 text-slate-700">
							<span>{line.name} × {line.quantity}</span>
							<span class="font-semibold text-slate-900"
								>{line.subtotal.toFixed(2)} zl</span
							>
						</li>
					{/each}
				</ul>
				<a
					href="/"
					class="mt-8 inline-flex rounded-2xl bg-slate-900 px-6 py-3 text-base font-semibold text-white shadow-lg transition hover:-translate-y-0.5 hover:bg-black"
				>
					Wróć do sklepu
				</a>
			</div>
		{:else if !cart.isEmpty}
			<ul class="mt-8 flex flex-col gap-4">
				{#each cart.items as item (item.product.id)}
					<CartItem {item} />
				{/each}
			</ul>

			<div
				class="mt-10 flex flex-col items-end gap-4 border-t border-slate-200 pt-8"
			>
				{#if checkoutError}
					<p
						class="w-full max-w-lg rounded-xl bg-red-50 px-4 py-3 text-right text-sm text-red-800 ring-1 ring-red-200"
					>
						{checkoutError}
					</p>
				{/if}
				<p class="text-xl font-bold text-slate-700">
					Razem ({cart.totalItems} szt.):
					<span class="ml-2 text-2xl text-slate-900">
						{cart.totalPrice.toFixed(2)} zl
					</span>
				</p>
				<button
					type="button"
					disabled={checkoutLoading}
					class="inline-flex items-center justify-center rounded-2xl bg-slate-900 px-8 py-4 text-lg font-semibold text-white shadow-lg shadow-slate-900/30 transition hover:-translate-y-0.5 hover:bg-black cursor-pointer disabled:pointer-events-none disabled:opacity-50"
					onclick={() => void handleCheckout()}
				>
					{checkoutLoading ? "Przetwarzanie…" : "Przejdź do płatności"}
				</button>
			</div>
		{:else}
			<div
				class="mt-12 rounded-3xl bg-white/80 p-12 text-center shadow-xl ring-1 ring-slate-200/80 backdrop-blur"
			>
				<p class="text-slate-600">
					Dodaj produkty z listy, aby zobaczyć je tutaj.
				</p>
				<a
					href="/"
					class="mt-6 inline-flex rounded-2xl bg-slate-900 px-6 py-3 text-base font-semibold text-white shadow-lg transition hover:-translate-y-0.5 hover:bg-black"
				>
					Przejdź do sklepu
				</a>
			</div>
		{/if}
	</div>
</section>
