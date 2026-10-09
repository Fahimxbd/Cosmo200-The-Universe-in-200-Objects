# Cosmo200: The Universe in 200 Objects

A free, MIT-licensed astronomy atlas for schools, colleges, universities, and curious minds. Built with **React 18, Vite, React Three Fiber, Three.js, Drei, Tailwind CSS, and Framer Motion**. Hosting targets **Cloudflare Workers only**, with source and CI on **GitHub**.

## Live Website

[**Explore Cosmo200 on Cloudflare Workers →**](https://cosmo200-the-universe-in-200-objects.fahimprivateuser-d8a.workers.dev/)

## Explore

- Exactly **200 unique named objects** in local `public/data/objects.json`, served at `/data/objects.json`.
- Six collections: Universe (1), Superclusters (5), Galaxies (20), Nebulae and Star Clusters (30), Star Systems (50), Planets and Moons (94).
- Click 3D objects, use the keyboard-accessible catalogue, or search names and aliases (try `Search Andromeda` or `M31`).
- Smooth camera flights, orbit controls, touch pinch zoom, reset view, and an **all 200 objects** overview.
- Object information with NASA archive images where a relevant match is available, original media links and credits, and explicit unavailable-image states.
- Six-stop educational tour with automatic transitions, text, optional browser speech, pause/resume, previous/next, and direct stop selection. Speech availability depends on the browser/OS. No audio is recorded.
- Responsive desktop sidebar and mobile explorer drawer/object sheet.
- Eco mode by default: DPR 1, lower point count, distance-based LOD, shared particle geometry, on-demand rendering, no shadows, no postprocessing, and lazy-loaded 3D code. Only the selected collection renders unless all-object overview is enabled. Decorative background points are not additional catalogue objects.

## Scientific scope

**This is a schematic educational atlas, not a physical simulation.** Coordinates, sizes, colors, and camera distances are illustrative, not measured astronomical positions. Collection transitions represent six educational scales rather than one physically nested containment tree. The Sun is kept in the final collection to preserve the supplied ID scheme. Star Systems includes individual stars and multiple-star systems. The observable universe is roughly 92 billion light-years across today; its age is about 13.8 billion years.

Images from the NASA archive may be telescope composites, artist impressions, diagrams, or images containing a broader region. They are not always direct photographs of the selected object. Some minor moons and other objects have no verified archive match; the application clearly reports that instead of inventing an image. Use each image's linked original caption for full interpretation and credit. NASA does not endorse this application. NASA/partner images retain their applicable usage terms; the MIT license covers this project's code, not third-party media.

Reference starting points:
- [NASA: How big is space?](https://www.nasa.gov/science-research/astrophysics/how-big-is-space-we-asked-a-nasa-expert-episode-61/)
- [NASA Universe](https://science.nasa.gov/universe/)
- [NASA Solar System](https://science.nasa.gov/solar-system/)
- [NASA Image and Video Library](https://images.nasa.gov/)

## Run locally

Node.js 22 or later:

```sh
npm ci
npm run dev
npm test
npm run build
npm run preview
```

No API key, account, database, analytics, or paid service is needed to explore. Catalogue and fonts are local; NASA images need an internet connection. Search and educational text continue to work if an image fails. A non-WebGL fallback preserves the searchable catalogue.


## Android / Termux setup

You can clone and run the React/Vite project **locally on an Android phone with Termux**. This starts a development website in your phone's browser; it **does not install an Android APK** or replace the public Cloudflare Workers deployment.

1. Install a current Termux release from [F-Droid](https://f-droid.org/packages/com.termux/) or the official [Termux GitHub releases](https://github.com/termux/termux-app/releases). Open Termux and run:

   ```sh
   pkg update -y && pkg upgrade -y
   pkg install -y git nodejs-lts
   node --version
   npm --version
   ```

   Use Node.js **22.12 or later** (check the reported version). If your package repository provides an older version, update Termux/package repositories before continuing.

2. Download the project and install its dependencies:

   ```sh
   cd ~
   git clone https://github.com/Fahimxbd/Cosmo200-The-Universe-in-200-Objects.git
   cd Cosmo200-The-Universe-in-200-Objects
   npm ci
   ```

3. Start the local Vite development server:

   ```sh
   npm run dev -- --port 5173
   ```

   Open **http://127.0.0.1:5173/** in Chrome or another Android browser on the **same phone**. Leave the Termux session running while you use the site. You can also run `termux-open-url http://127.0.0.1:5173/` in a separate Termux session. Press **Ctrl+C** in the server session to stop it.

4. Optional — on a later visit, update the checkout:

   ```sh
   cd ~/Cosmo200-The-Universe-in-200-Objects
   git pull --ff-only
   npm ci
   npm run dev -- --port 5173
   ```

   `git pull --ff-only` requires a clean, compatible checkout; save any local edits before updating.

You can optionally run `npm test` and `npm run build` after installation. **Note:** Vite/Rollup and other development dependencies may use platform-specific native packages; Android/Termux compatibility is not guaranteed for every device or architecture. Rendering also depends on browser WebGL support and your phone's GPU. If installation fails due to a native package, use a supported desktop/Linux build environment or the public [Cloudflare Workers website](https://cosmo200-the-universe-in-200-objects.fahimprivateuser-d8a.workers.dev/) instead.


## Deploy to Cloudflare Workers

### Cloudflare Workers Builds (dashboard)

Connect this GitHub repository to a new Worker named **cosmo200**.

- Root directory: repository root
- Production branch: `main`
- Build command: `npm run build`
- Deploy command: `npx wrangler deploy`

`wrangler.jsonc` serves `dist` using Workers Static Assets with SPA fallback. No Cloudflare Pages, external host, database, or runtime secrets are required. Cloudflare Workers website: [**https://cosmo200-the-universe-in-200-objects.fahimprivateuser-d8a.workers.dev/**](https://cosmo200-the-universe-in-200-objects.fahimprivateuser-d8a.workers.dev/). Verify the deployment using the checklist below.

### GitHub Actions alternative

In GitHub repository Settings → Secrets and variables → Actions, configure:

- `CLOUDFLARE_API_TOKEN`: an account-scoped token allowed to edit Workers for your account.
- `CLOUDFLARE_ACCOUNT_ID`: your target Cloudflare account ID.

The `Deploy to Cloudflare Workers` workflow builds, tests, and publishes after pushes to `main` or manual dispatch. Use **one** automatic deployment route (Workers Builds or Actions), not both. Never commit credentials. Missing credentials deliberately fail the workflow with an explanatory error, rather than claiming a deployment succeeded.

Alternatively, after authenticating Wrangler locally:

```sh
npx wrangler login
npm run deploy
```

After deployment, verify the returned HTTPS URL, `/data/objects.json` (200 records), search for Andromeda, visit every collection, and run the six-stop tour. GitHub build success alone is not deployment proof.

## Folder structure

```text
cosmo200/
├── .github/workflows/
│   ├── ci.yml                 # Build, tests, downloadable build artifact
│   └── deploy.yml             # Cloudflare Workers deployment
├── public/
│   ├── data/objects.json      # Complete 200-object catalogue and media metadata
│   ├── _headers
│   └── favicon.svg
├── src/
│   ├── App.jsx               # Application state, level navigation, tour orchestration
│   ├── catalogue.js          # Search, validation, level and tour definitions
│   ├── main.jsx
│   ├── styles.css
│   └── components/
│       ├── UniverseCanvas.jsx # R3F scene, LOD objects, particles, smooth camera
│       ├── Sidebar.jsx        # Search, collection navigation, accessible catalogue
│       ├── InfoPanel.jsx      # NASA image, context, credit, object actions
│       └── Tour.jsx           # Tour text and playback controls
├── scripts/
│   ├── catalogue.py           # Rebuild curated data (resets media metadata)
│   ├── resolve-images.py      # Initial NASA archive discovery
│   ├── refine-images.py       # Refine media searches; review matches before publishing
│   └── validate-data.mjs
├── tests/catalogue.test.mjs
├── index.html
├── package.json
├── package-lock.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── wrangler.jsonc
└── LICENSE
```

## Contribute

Open a pull request for scientific corrections, translations, accessibility improvements, or better source/image matches. Preserve the 200-object count and stable IDs. Run `npm test` and `npm run build`. Review astronomy content with an educator before using it as assessed course material. Performance depends on device and browser; no specific low-end frame rate is guaranteed.

Copyright © 2026 Fahim Sikder. Code licensed under MIT.
