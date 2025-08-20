<script lang="ts">
    const links = [
        { href: "/", label: "Accueil" },
        { href: "/equipe", label: "Equipe" },
        { href: "/services", label: "Services" },
        { href: "/formations", label: "Formations" },
        { href: "/partenaires", label: "Partenaires" },
        { href: "/contact", label: "Contact" },
    ];

    let isOpen = $state(false);

    function toggleMenu() {
        isOpen = !isOpen;
    }

    // One key shortcut per link
    document.addEventListener("keydown", (event) => {
        // Don't catch shortcuts with Ctrl, Alt, Meta, Shift, and repeat (holding down a key)
        if (
            event.ctrlKey ||
            event.altKey ||
            event.metaKey ||
            event.shiftKey ||
            event.repeat
        )
            return;
        for (const link of links) {
            if (event.key.toLowerCase() === link.label.at(0)?.toLowerCase()) {
                window.location.href = link.href;
            }
        }
    });
</script>

<nav>
    <button class="burger" onclick={toggleMenu} aria-label="Menu">
        <span class:is-open={isOpen}></span>
        <span class:is-open={isOpen}></span>
        <span class:is-open={isOpen}></span>
    </button>

    <ol class:open={isOpen}>
        {#each links as link}
            <li>
                <a href={link.href}>
                    <code>
                        {#if window.location.pathname === link.href}
                            <u>{link.label}</u>
                        {:else}
                            <u>{link.label.at(0)}</u>{link.label.substring(1)}
                        {/if}
                    </code>
                </a>
            </li>
        {/each}
    </ol>
</nav>

<style>
    nav {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        border-radius: 12px;
        border: 1px solid
            color-mix(in srgb, var(--primary-color) 11%, transparent);
        background-color: color-mix(
            in srgb,
            var(--primary-color) 10%,
            transparent
        );
        backdrop-filter: blur(4px);
        margin: 1rem auto;
        padding: 0.75rem 1.5rem;
        width: fit-content;
        position: relative;
    }

    ol {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        list-style-type: none;
        gap: 2rem;
        padding: 0;
        transition: max-height 0.3s ease;
    }

    .burger {
        display: none;
        flex-direction: column;
        gap: 5px;
        background: none;
        border: none;
        cursor: pointer;
        padding: 0.5rem;
    }

    .burger span {
        width: 25px;
        height: 2px;
        background-color: var(--primary-color);
        transition:
            transform 0.3s,
            opacity 0.3s;
    }

    .burger span.is-open:nth-child(1) {
        transform: translateY(7px) rotate(45deg);
    }
    .burger span.is-open:nth-child(2) {
        opacity: 0;
    }
    .burger span.is-open:nth-child(3) {
        transform: translateY(-7px) rotate(-45deg);
    }

    @media screen and (max-width: 768px) {
        .burger {
            display: flex;
        }

        ol {
            flex-direction: column;
            max-height: 0;
            overflow: hidden;
            display: none;
        }

        ol.open {
            max-height: 500px;
            display: flex;
        }
    }

    a {
        text-decoration: none;
    }
</style>
