<script lang="ts">
  import type { PageData } from "./$types";

  let { data }: { data: PageData } = $props();
  const products = $derived(data.products ?? []);

  let quantities = $state<Record<number, number>>({});

  $effect(() => {
    for (const p of products) {
      if (quantities[p.id] === undefined) {
        quantities[p.id] = 1;
      }
    }
  });

  function getQuantity(productId: number): number {
    const q = quantities[productId];
    return q === undefined ? 1 : q;
  }

  function setQuantity(productId: number, value: number): void {
    quantities[productId] = Math.max(0, value);
  }

  function removeFromCart(productId: number): void {
    quantities[productId] = 0;
  }

  const cartProducts = $derived(products.filter((p) => getQuantity(p.id) > 0));

  const totalItems = $derived(
    cartProducts.reduce((sum, p) => sum + getQuantity(p.id), 0),
  );
  const totalPrice = $derived(
    cartProducts.reduce((sum, p) => sum + p.price * getQuantity(p.id), 0),
  );
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
      {cartProducts.length === 0
        ? "Brak produktów w koszyku."
        : `${cartProducts.length} ${cartProducts.length === 1 ? "produkt" : "produktów"} w koszyku.`}
    </p>

    {#if cartProducts.length > 0}
      <ul class="mt-8 flex flex-col gap-4">
        {#each cartProducts as product (product.id)}
          <li
            class="flex items-center gap-4 overflow-hidden rounded-2xl bg-white p-4 shadow-xl ring-1 ring-slate-200 transition hover:shadow-slate-900/10 md:gap-6 md:p-5"
          >
            <div
              class="relative h-20 w-20 shrink-0 overflow-hidden rounded-xl bg-slate-100 md:h-24 md:w-24"
            >
              <img
                src={`https://picsum.photos/seed/product-${product.id}/200/200`}
                alt={`Zdjęcie produktu ${product.name}`}
                class="h-full w-full object-cover"
              />
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex flex-wrap items-center justify-between gap-2">
                <h2 class="text-lg font-bold text-slate-900">{product.name}</h2>
                <div class="flex items-center gap-2">
                  <div
                    class="flex items-center gap-1 rounded-xl border border-slate-200 bg-slate-50 px-1 py-0.5"
                    role="group"
                    aria-label="Ilość"
                  >
                    <button
                      type="button"
                      class="h-8 w-8 rounded-lg bg-white text-lg font-semibold text-slate-700 shadow ring-1 ring-slate-200 transition hover:bg-slate-100 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                      onclick={() =>
                        setQuantity(product.id, getQuantity(product.id) - 1)}
                      disabled={getQuantity(product.id) <= 0}
                      aria-label="Zmniejsz ilość"
                    >
                      −
                    </button>
                    <span
                      class="min-w-[2rem] text-center text-base font-bold text-slate-900"
                    >
                      {getQuantity(product.id)}
                    </span>
                    <button
                      type="button"
                      class="h-8 w-8 rounded-lg bg-white text-lg font-semibold text-slate-700 shadow ring-1 ring-slate-200 transition hover:bg-slate-100 cursor-pointer"
                      onclick={() =>
                        setQuantity(product.id, getQuantity(product.id) + 1)}
                      aria-label="Zwiększ ilość"
                    >
                      +
                    </button>
                  </div>
                  <button
                    type="button"
                    class="rounded-xl border border-red-200 bg-white p-2 text-red-600 transition hover:bg-red-50 hover:border-red-300 cursor-pointer"
                    onclick={() => removeFromCart(product.id)}
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
                {product.description}
              </p>
              <p class="mt-2 text-xl font-black tracking-tight text-slate-900">
                {(product.price * getQuantity(product.id)).toFixed(2)} zl
              </p>
            </div>
          </li>
        {/each}
      </ul>

      <div
        class="mt-10 flex flex-col items-end gap-4 border-t border-slate-200 pt-8"
      >
        <p class="text-xl font-bold text-slate-700">
          Razem ({totalItems} szt.):
          <span class="ml-2 text-2xl text-slate-900">
            {totalPrice.toFixed(2)} zl
          </span>
        </p>
        <button
          type="button"
          class="inline-flex items-center justify-center rounded-2xl bg-slate-900 px-8 py-4 text-lg font-semibold text-white shadow-lg shadow-slate-900/30 transition hover:-translate-y-0.5 hover:bg-black cursor-pointer"
        >
          Przejdź do płatności (placeholder)
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
