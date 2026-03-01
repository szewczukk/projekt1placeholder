<script lang="ts">
	import { products } from "$lib/constants/products";
</script>

<ul class="flex gap-8">
  {#each products as product}
    <li>
        <a href={`/products/${product.id}`}>
            <div class="w-[256px] h-[256px] bg-slate-300"></div>
            <div class="flex justify-between">
                <p>{product.name}</p>
                <p>{product.price}zł</p>
            </div>
        </a>
    </li>
  {/each}
</ul>
