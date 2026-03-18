<script lang="ts">
	import CartItem from "$lib/components/checkout/CartItem.svelte";
	import { cart } from "$lib/stores/cart.svelte";
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
			{cart.isEmpty
				? "Brak produktów w koszyku."
				: `${cart.items.length} ${cart.items.length === 1 ? "produkt" : "produktów"} w koszyku.`}
		</p>

		{#if !cart.isEmpty}
			<ul class="mt-8 flex flex-col gap-4">
				{#each cart.items as item (item.product.id)}
					<CartItem {item} />
				{/each}
			</ul>

			<div
				class="mt-10 flex flex-col items-end gap-4 border-t border-slate-200 pt-8"
			>
				<p class="text-xl font-bold text-slate-700">
					Razem ({cart.totalItems} szt.):
					<span class="ml-2 text-2xl text-slate-900">
						{cart.totalPrice.toFixed(2)} zl
					</span>
				</p>
				<button
					type="button"
					class="inline-flex items-center justify-center rounded-2xl bg-slate-900 px-8 py-4 text-lg font-semibold text-white shadow-lg shadow-slate-900/30 transition hover:-translate-y-0.5 hover:bg-black cursor-pointer"
					onclick={() => cart.checkout()}
				>
					Przejdź do płatności
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
