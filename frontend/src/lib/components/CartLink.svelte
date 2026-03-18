<script lang="ts">
	import { cart } from "$lib/stores/cart.svelte";
</script>

<a
	href="/checkout"
	class="relative rounded-full bg-slate-900 px-5 py-2 text-sm font-semibold text-white shadow-lg shadow-slate-900/20 transition hover:-translate-y-0.5 hover:bg-black"
>
	Koszyk
	{#if cart.totalItems > 0}
		<span
			class="absolute -right-2 -top-2 flex h-5 min-w-5 items-center justify-center rounded-full bg-red-500 px-1.5 text-xs font-bold text-white shadow"
		>
			{cart.totalItems}
		</span>
	{/if}
</a>
