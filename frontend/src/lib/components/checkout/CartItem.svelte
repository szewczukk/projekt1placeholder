<script lang="ts">
	import { type CartItem, cart } from "$lib/stores/cart.svelte";

	let { item }: { item: CartItem } = $props();
</script>

<li
	class="flex items-center gap-4 overflow-hidden rounded-2xl bg-white p-4 shadow-xl ring-1 ring-slate-200 transition hover:shadow-slate-900/10 md:gap-6 md:p-5"
>
	<div
		class="relative h-20 w-20 shrink-0 overflow-hidden rounded-xl bg-slate-100 md:h-24 md:w-24"
	>
		<img
			src={`https://picsum.photos/seed/product-${item.product.id}/200/200`}
			alt={`Zdjęcie produktu ${item.product.name}`}
			class="h-full w-full object-cover"
		/>
	</div>
	<div class="min-w-0 flex-1">
		<div class="flex flex-wrap items-center justify-between gap-2">
			<h2 class="text-lg font-bold text-slate-900">{item.product.name}</h2>
			<div class="flex items-center gap-2">
				<div
					class="flex items-center gap-1 rounded-xl border border-slate-200 bg-slate-50 px-1 py-0.5"
					role="group"
					aria-label="Ilość"
				>
					<button
						type="button"
						class="h-8 w-8 rounded-lg bg-white text-lg font-semibold text-slate-700 shadow ring-1 ring-slate-200 transition hover:bg-slate-100 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
						onclick={() => void cart.updateQuantity(item.product.id, item.quantity - 1)}
						disabled={item.quantity <= 1}
						aria-label="Zmniejsz ilość"
					>
						−
					</button>
					<span class="min-w-[2rem] text-center text-base font-bold text-slate-900">
						{item.quantity}
					</span>
					<button
						type="button"
						class="h-8 w-8 rounded-lg bg-white text-lg font-semibold text-slate-700 shadow ring-1 ring-slate-200 transition hover:bg-slate-100 cursor-pointer"
						onclick={() => void cart.updateQuantity(item.product.id, item.quantity + 1)}
						aria-label="Zwiększ ilość"
					>
						+
					</button>
				</div>
				<button
					type="button"
					class="rounded-xl border border-red-200 bg-white p-2 text-red-600 transition hover:bg-red-50 hover:border-red-300 cursor-pointer"
					onclick={() => void cart.removeItem(item.product.id)}
					aria-label="Usuń z koszyka"
					title="Usuń z koszyka"
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-5 w-5"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
						aria-hidden="true"
						focusable="false"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
						/>
					</svg>
				</button>
			</div>
		</div>
		<p class="mt-0.5 text-sm text-slate-600 line-clamp-2">
			{item.product.description}
		</p>
		<p class="mt-2 text-xl font-black tracking-tight text-slate-900">
			{(item.product.price * item.quantity).toFixed(2)} zl
		</p>
	</div>
</li>
