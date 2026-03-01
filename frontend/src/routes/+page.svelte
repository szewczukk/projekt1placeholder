<script lang="ts">
const products = [
	{
		id: 1,
		name: "Product 1",
		price: 100,
	},
	{
		id: 2,
		name: "Product 2",
		price: 150,
	},
	{
		id: 2,
		name: "Product 3",
		price: 400,
	},
];
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
