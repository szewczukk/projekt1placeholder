<script lang="ts">
	import type { Product } from "$lib/api/products";
	import type { PageData } from "./$types";

	let { data }: { data: PageData } = $props();
	const products = $derived(data.products as Product[]);
</script>

<ul class="flex gap-8">
  {#each products as product}
    <li>
        <a href={`/products/${product.id}`}>
        <img src="https://picsum.photos/seed/${product.id}/256/256" alt={product.name} class="w-[256px] h-[256px]" />
            <div class="flex justify-between">
                <p>{product.name}</p>
                <p>{product.price}zł</p>
            </div>
        </a>
    </li>
  {/each}
</ul>
