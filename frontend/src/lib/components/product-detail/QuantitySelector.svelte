<script lang="ts">
type Props = {
	quantity: number;
	onIncrement: () => void;
	onDecrement: () => void;
};

let { quantity, onIncrement, onDecrement }: Props = $props();
</script>

<div
	class="flex items-center justify-between rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3"
>
	<span class="text-sm font-semibold uppercase tracking-wide text-slate-500">Ilość</span>
	<div class="flex items-center gap-3">
		<button
			type="button"
			class="h-10 w-10 rounded-xl bg-white text-2xl font-semibold text-slate-700 shadow ring-1 ring-slate-200 transition hover:bg-slate-100 cursor-pointer"
			onclick={onDecrement}
			aria-label="Zmniejsz ilość"
		>
			-
		</button>
		<span class="w-10 text-center text-xl font-bold text-slate-900">{quantity}</span>
		<button
			type="button"
			class="h-10 w-10 rounded-xl bg-white text-2xl font-semibold text-slate-700 shadow ring-1 ring-slate-200 transition hover:bg-slate-100 cursor-pointer"
			onclick={onIncrement}
			aria-label="Zwiększ ilość"
		>
			+
		</button>
	</div>
</div>
