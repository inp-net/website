// @ts-check
import { defineConfig } from "astro/config";

import svelte from "@astrojs/svelte";

import mdx from "@astrojs/mdx";

// https://astro.build/config
export default defineConfig({
    integrations: [svelte(), mdx()],
    site: "https://net7.dev",
    outDir: "public",
    publicDir: "static",
});
