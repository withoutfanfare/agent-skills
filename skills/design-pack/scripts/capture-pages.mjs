#!/usr/bin/env node
/**
 * Capture full-page screenshots of a list of routes for a design pack.
 *
 * Written against the project's browser automation tool, such as
 * Playwright, because most projects that need this already have one
 * installed as a dev dependency. Swap the launch/navigate calls below for
 * whichever tool the project actually uses if it differs.
 *
 * Before the shot, it settles the page rather than trusting a fixed delay:
 * waits for network idle, forces lazy images to load eagerly, opens any
 * scroll-triggered reveal animations, and freezes CSS animations and
 * transitions. Without this a full-page capture routinely shows a half
 * faded-in section or a blank gap where a lazy image had not arrived yet.
 *
 * Usage:
 *   node scripts/capture-pages.mjs --base https://example.test \
 *     --out design-pack/screenshots --routes / /catalogue /product/example
 *
 *   node scripts/capture-pages.mjs --config routes.json \
 *     --out design-pack/screenshots
 *
 * A config file (--config) is a JSON array, either plain route strings or
 * { "route": "/product/example", "name": "product-detail" } objects, for
 * routes whose auto-generated filename would be awkward.
 *
 * Flags:
 *   --base <url>       required unless every route in --config is absolute
 *   --out <dir>         output directory (default: ./screenshots)
 *   --routes <r...>      one or more routes, space separated
 *   --config <file>      JSON file of routes (alternative to --routes)
 *   --width <n>           viewport width in px (default: 1440)
 *   --prefix <text>        filename prefix, e.g. "mobile-" (default: "")
 *   --reveal <a:b,c:d>      hidden-class:shown-class pairs to force open
 *                            (default: "reveal:in")
 */

import { mkdir } from 'node:fs/promises';
import path from 'node:path';

function parseArgs(argv) {
    const opts = { routes: [], width: 1440, prefix: '', out: 'screenshots', reveal: 'reveal:in' };
    for (let i = 0; i < argv.length; i++) {
        const arg = argv[i];
        if (arg === '--base') opts.base = argv[++i];
        else if (arg === '--out') opts.out = argv[++i];
        else if (arg === '--config') opts.config = argv[++i];
        else if (arg === '--width') opts.width = Number(argv[++i]);
        else if (arg === '--prefix') opts.prefix = argv[++i];
        else if (arg === '--reveal') opts.reveal = argv[++i];
        else if (arg === '--routes') {
            while (argv[i + 1] && !argv[i + 1].startsWith('--')) opts.routes.push(argv[++i]);
        }
    }
    return opts;
}

async function loadRoutes(opts) {
    if (opts.config) {
        const { readFile } = await import('node:fs/promises');
        const raw = JSON.parse(await readFile(opts.config, 'utf8'));
        return raw.map((entry) =>
            typeof entry === 'string' ? { route: entry, name: slugify(entry) } : { name: slugify(entry.route), ...entry });
    }
    if (opts.routes.length === 0) {
        throw new Error('Give routes with --routes <path...> or --config <file.json>');
    }
    return opts.routes.map((route) => ({ route, name: slugify(route) }));
}

function slugify(route) {
    return route === '/' ? 'home' : route.replace(/^\//, '').replace(/\/$/, '').replace(/\//g, '-') || 'home';
}

async function settlePage(page, revealPairs) {
    await page.waitForLoadState('networkidle').catch(() => {
        // A page with a long-lived connection (websocket, polling) never
        // reaches network idle; fall through and settle by DOM state instead.
    });
    await page.evaluate((pairs) => {
        // Freeze animations and transitions so the shot is not mid-motion.
        const style = document.createElement('style');
        style.textContent = '*, *::before, *::after { animation-duration: 0s !important; animation-delay: 0s !important; transition-duration: 0s !important; }';
        document.head.appendChild(style);

        for (const [hidden, shown] of pairs) {
            for (const el of document.querySelectorAll(`.${hidden}`)) el.classList.add(shown);
        }
        // Lazy-loaded <img> tags can still be blank placeholders when the shot
        // fires; force them to load now instead of waiting on scroll position.
        for (const img of Array.from(document.images)) {
            if (img.loading === 'lazy') img.loading = 'eager';
        }
    }, revealPairs);
    // Give eagerly-switched images a moment to actually finish decoding.
    await page.waitForTimeout(500);
}

async function main() {
    const opts = parseArgs(process.argv.slice(2));
    const routes = await loadRoutes(opts);
    const revealPairs = opts.reveal.split(',').filter(Boolean).map((pair) => pair.split(':'));

    await mkdir(opts.out, { recursive: true });

    const { chromium } = await import('playwright');
    const browser = await chromium.launch();
    const page = await browser.newPage({ viewport: { width: opts.width, height: 900 } });

    let failures = 0;
    for (const { route, name } of routes) {
        const url = /^https?:\/\//.test(route) ? route : new URL(route, opts.base).href;
        const file = path.join(opts.out, `${opts.prefix}${name}.jpg`);
        try {
            await page.goto(url, { waitUntil: 'load', timeout: 30_000 });
            await settlePage(page, revealPairs);
            await page.screenshot({ path: file, fullPage: true, type: 'jpeg', quality: 90 });
            const height = await page.evaluate(() => document.documentElement.scrollHeight);
            console.log(`${name}  ${opts.width}x${height}  -> ${file}`);
        } catch (captureError) {
            failures += 1;
            console.error(`${name}: capture failed - ${captureError.message}`);
        }
    }

    await browser.close();
    process.exit(failures > 0 ? 1 : 0);
}

main().catch((err) => {
    console.error(err.stack || err.message);
    process.exit(1);
});
