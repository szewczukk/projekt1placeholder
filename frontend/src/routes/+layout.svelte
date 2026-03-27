<script lang="ts">
import { onMount } from "svelte";
import favicon from "$lib/assets/favicon.svg";
import { ensureSession } from "$lib/session";
import "../app.css";

let { children } = $props();

onMount(() => {
	void ensureSession();
});
</script>

<svelte:head> <link rel="icon" href={favicon}> </svelte:head>

<div class="h-full w-full">{@render children()}</div>
