<script lang="ts">
type Props = {
	name: string;
	imageUrl: string;
};

let { name, imageUrl }: Props = $props();
let isLoading = $state(false);
let hasError = $state(false);

$effect(() => {
	imageUrl;
	isLoading = true;
	hasError = false;
});
</script>

<div
	class="relative overflow-hidden rounded-3xl bg-white/70 p-3 shadow-2xl ring-1 ring-white/60 backdrop-blur"
>
	{#if hasError}
		<div
			class="flex h-[52vh] w-full items-center justify-center rounded-2xl bg-slate-200 text-center text-slate-500 md:h-[65vh]"
		>
			<div>
				<p class="text-sm uppercase tracking-[0.2em]">Brak podglądu</p>
				<p class="mt-2 text-lg font-semibold text-slate-600">{name}</p>
			</div>
		</div>
	{:else}
		<img
			src={imageUrl}
			alt={`Zdjecie produktu ${name}`}
			class={`h-[52vh] w-full rounded-2xl object-cover transition-opacity duration-500 md:h-[65vh] ${isLoading ? "opacity-0" : "opacity-100"}`}
			onload={() => (isLoading = false)}
			onerror={() => {
				isLoading = false;
				hasError = true;
			}}
		>
	{/if}

	{#if isLoading && !hasError}
		<div class="absolute inset-3 overflow-hidden rounded-2xl bg-slate-200">
			<div
				class="h-full w-full animate-pulse bg-gradient-to-r from-slate-200 via-slate-100 to-slate-200"
			></div>
		</div>
	{/if}

	<div
		class="pointer-events-none absolute inset-x-3 bottom-3 rounded-2xl bg-gradient-to-t from-black/50 to-transparent p-6"
	>
		<p class="text-xs uppercase tracking-[0.2em] text-white/80">Shop Collection</p>
		<p class="text-2xl font-bold text-white md:text-3xl">{name}</p>
	</div>
</div>
