<script lang="ts">
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

{#if product}
	<section class="bg-slate-100 px-12 py-8">
		<div class="mb-12 flex justify-end">
			<a href="/checkout" class="text-3xl uppercase tracking-wide">Koszyk</a>
		</div>

		<div class="flex items-start gap-14">
			<div class="flex h-[340px] w-[430px] items-center justify-center bg-slate-300 text-3xl text-slate-700">
				Zdjęcie produktu
			</div>

			<div class="pt-4">
				<h1 class="mb-3 text-4xl uppercase tracking-wide">{product.name}</h1>
				<p class="mb-8 text-2xl">{product.price}zł</p>

				<div class="flex items-center gap-6">
					<button
						type="button"
						class="bg-slate-300 px-8 py-4 text-3xl uppercase tracking-wide"
						onclick={handleAddToCart}
					>
						Dodaj do koszyka
					</button>
					<div class="flex items-center gap-3 bg-slate-300 px-4 py-4 text-3xl uppercase tracking-wide">
						<span>Ilość</span>
						<button type="button" class="px-3" onclick={decrementQuantity} aria-label="Zmniejsz ilość">
							-
						</button>
						<span>{quantity}</span>
						<button type="button" class="px-3" onclick={incrementQuantity} aria-label="Zwiększ ilość">
							+
						</button>
					</div>
				</div>
			</div>
		</div>
	</section>
{:else}
	<section class="bg-slate-100 p-12">
		<h1 class="mb-4 text-4xl uppercase">Produkt nie został znaleziony</h1>
		<a href="/products" class="underline">Wróć do produktów</a>
	</section>
{/if}
