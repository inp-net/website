<script lang="ts">
    import Website from "./icons/globe.svelte";
    import LinkedIn from "./icons/linkedin.svelte";
    import Discord from "./icons/discord.svelte";
    import Github from "./icons/github.svelte";

    let { name, title, avatar, links } = $props<{
        name: string;
        title: string;
        avatar?: string;
        links?: {
            linkedin?: string;
            github?: string;
            discord?: string;
            website?: string;
        };
    }>();
</script>

<div class="member">
    <img src={avatar} alt={`Avatar de ${name}`} class="avatar" />
    <div class="info">
        <h3>{name}</h3>
        <p>{title}</p>
        <div class="links">
            {#if links?.linkedin}
                <a href={links.linkedin} target="_blank" aria-label={`LinkedIn de ${name}`}>
                    <LinkedIn />
                </a>
            {/if}
            {#if links?.github}
                <a href={links.github} target="_blank" aria-label={`GitHub de ${name}`}>
                    <Github />
                </a>
            {/if}
            {#if links?.discord}
                <a href={links.discord} target="_blank" aria-label={`Discord de ${name}`}>
                    <Discord />
                </a>
            {/if}
            {#if links?.website}
                <a href={links.website} target="_blank" aria-label={`Website de ${name}`}>
                    <Website />
                </a>
            {/if}
        </div>
    </div>
</div>

<style>
    .member {
        display: flex;
        align-items: center;
        flex-direction: column;
        text-align: center;
    }

    .avatar {
        border-radius: 50%;
        margin-right: 1rem;
        aspect-ratio: 1 / 1;
        width: 10rem;
    }

    .links {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
    }

    .links a {
        width: 1.5rem;
        height: 1.5rem;
        fill: currentColor;
    }
</style>
