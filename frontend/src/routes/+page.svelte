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
      price: 200,
    },
  ];
</script>

<div class="container mx-auto">
  <ul class="flex gap-4">
    {#each products as product}
      <li>
        <div class="w-[256px] h-[256px] bg-slate-300"></div>
        <div>
          <p>{product.name}</p>
          <p>{product.price}</p>
        </div>
      </li>
    {/each}
  </ul>
</div>
