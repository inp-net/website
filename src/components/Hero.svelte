<script lang="ts">
    import words from "../content/words.json";

    let width = $state(window.innerWidth);
    let height = $state(window.innerHeight);

    function update() {
        width = window.innerWidth;
        height = window.innerHeight;
    }
    window.addEventListener("resize", update);

    let randomWords: string[] = $state([]);
    let fontHeight = $state(16);
    let gap = $state(0);

    $effect(() => {
        const jetbrainsMonoRatio = 0.48;
        fontHeight = (width / height) * 10;
        const fontWidth = fontHeight * jetbrainsMonoRatio;

        const wordLengthMean = words.reduce((sum, word) => sum + word.length, 0) / words.length;
        gap = fontWidth * 0.5;
        const wordWidthMean = wordLengthMean * fontWidth + gap;

        const lineCount = Math.ceil(height / (fontHeight + gap));
        const wordCount = Math.ceil(width / wordWidthMean) * lineCount;

        const pool: string[] = Array(Math.ceil(wordCount / words.length))
            .fill(words)
            .flat();

        randomWords = pool
            .slice(0, wordCount)
            .map((value) => ({ value, sort: Math.random() }))
            .sort((a, b) => a.sort - b.sort)
            .map(({ value }) => value);
    });
</script>

<div class="words" style:--heightPx={fontHeight + "px"} style:--gapPx={gap + "px"}>
    {#each Array(randomWords.length) as _, i}
        <span class="word">
            {randomWords[i % randomWords.length]}
        </span>
    {/each}
</div>

<div class="hero">
    <code>L'ASSOCIATION D'INFORMATIQUE DE L'ENSEEIHT</code>
</div>

<style>
    .hero {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100vh;
    }

    code {
        position: absolute;
        text-align: center;
        font-size: 16;
        bottom: 10rem;
    }

    .words {
        position: absolute;
        height: 100%;
        width: 100%;
        overflow: hidden;
        top: 0;
        display: flex;
        gap: var(--gapPx);
        flex-wrap: wrap;
        justify-content: space-around;
        font-size: var(--heightPx);
        background:
            center bottom / 100vw url("../assets/fade.svg"),
            center / min(95vw, 60rem) url("../assets/net7_bloom.svg"),
            left top / 75vw 75vh url("../assets/blob1.svg"),
            right bottom / 75vw 75vh url("../assets/blob2.svg");
        background-repeat: no-repeat;
        background-clip: text;
        line-height: 0.75;
        color: transparent;
        user-select: none;
    }

    .word:hover {
        color: var(--primary-color);
    }
</style>
