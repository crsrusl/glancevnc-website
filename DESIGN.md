---
name: GlanceVNC
description: Computer exhibition — real software, clear connections.
colors:
  blue: "#1645ed"
  blue-deep: "#1035b8"
  ink: "#101d36"
  muted: "#526078"
  paper: "#f8faff"
  sky: "#dfeeff"
  line: "#d6dfea"
  white: "#fff"
typography:
  display:
    fontFamily: '"Schibsted Grotesk", Arial, sans-serif'
    fontSize: "clamp(3.15rem, 6.1vw, 5.6rem)"
    fontWeight: 650
    lineHeight: 1.08
    letterSpacing: "-0.035em"
  headline:
    fontFamily: '"Schibsted Grotesk", Arial, sans-serif'
    fontSize: "clamp(2.25rem, 4vw, 3.75rem)"
    fontWeight: 650
    lineHeight: 1.08
    letterSpacing: "-0.035em"
  title:
    fontFamily: '"Schibsted Grotesk", Arial, sans-serif'
    fontSize: "1.4rem"
    fontWeight: 650
    lineHeight: 1.08
    letterSpacing: "-0.025em"
  body:
    fontFamily: '"Schibsted Grotesk", Arial, sans-serif'
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: '"Schibsted Grotesk", Arial, sans-serif'
    fontSize: "0.9rem"
    fontWeight: 550
rounded:
  control: "6px"
  button: "7px"
  surface: "12px"
spacing:
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "48px"
components:
  button-primary:
    backgroundColor: "{colors.blue}"
    textColor: "{colors.white}"
    rounded: "{rounded.button}"
    padding: "13px 22px"
  button-primary-hover:
    backgroundColor: "{colors.blue-deep}"
  button-light:
    backgroundColor: "{colors.white}"
    textColor: "{colors.blue-deep}"
    rounded: "{rounded.button}"
    padding: "13px 22px"
  button-outline:
    backgroundColor: "transparent"
    textColor: "inherit"
    rounded: "{rounded.button}"
    padding: "13px 22px"
  search-field:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "15px 17px"
  setup-surface:
    backgroundColor: "{colors.white}"
    rounded: "{rounded.surface}"
    padding: "36px"
  platform-tab:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "12px 23px"
---

# Design System: GlanceVNC

## Overview

**Creative North Star: "Computer exhibition"**

Computer exhibition presents the real app in solid blue fields, with cool white reading space and navy lettering. Large, tightly spaced grotesk headlines give the site confidence; quieter body text and precise dividers keep setup and compatibility information approachable.

The same system serves first-time visitors and experienced remote desktop users. Product imagery remains genuine, while Support, Privacy and Guides use clear white reading surfaces instead of repeating the promotional hero treatment.

**Key Characteristics:**
- Solid exhibition blue and generous real product imagery.
- One self-hosted type family with a distinct display and reading hierarchy.
- Flat reading surfaces, precise dividers and restrained rounded controls.
- Visible keyboard focus and progressively enhanced native interactions.

## Colors

A saturated blue accent sits against cool whites and deep navy; the frontmatter records the implemented CSS custom properties.

### Primary
- **Exhibition Blue** (`blue`): hero and download fields, primary actions, selected platform tabs, selection and focus.
- **Deep Exhibition Blue** (`blue-deep`): primary hover, reading links and selected navigation text.

### Neutral
- **Navy Ink** (`ink`): headings, body defaults, dark navigation action and device frame.
- **Slate** (`muted`): supporting copy, metadata and longer answers.
- **Cool Paper** (`paper`): footer, unselected platform controls and empty-search region.
- **Pale Sky** (`sky`): setup background, guide contents, help callouts and hover fills.
- **Fine Rule** (`line`): section, table, FAQ and header dividers.
- **Reading White** (`white`): reading pages, navigation, setup workbench and text on blue.

**The Clear Reading Rule.** Keep extended instructions on white; use sky for bounded help and setup regions, and blue for exhibition and acquisition fields.

## Typography

**Display and Body Font:** self-hosted Schibsted Grotesk, with Arial and sans-serif fallbacks. The variable font supplies weights 400–900 with `font-display: swap`; its OFL license is retained in `assets/fonts/OFL.txt`. Code uses `ui-monospace, SFMono-Regular, monospace`.

**Character:** compact, confident display lettering shares its underlying family with readable, neutral help copy. Sentence case carries the hierarchy.

### Hierarchy
- **Display:** the frontmatter scale is the base h1. The homepage adapts at 1100px, 800px and 540px, ending at `clamp(2.75rem, 11vw, 3.85rem)` on phones. Reading-page h1 becomes 3rem; guide-article h1 becomes 2.6rem on phones.
- **Headline:** the base h2 scale; article section headings use 2rem, then 1.7rem on phones.
- **Title:** base h3, with local sizes for setup, benefits and article subheads.
- **Body:** base text follows the frontmatter; introductory copy ranges from 1.08–1.2rem. Guide paragraphs use 1.8 line-height. Privacy paragraphs and FAQ answers are capped at 74ch.
- **Label:** navigation uses the frontmatter label role; metadata and captions remain smaller and quieter. Button labels use weight 600.

## Layout

The shared container is `min(100% - 80px, 1280px)`; reading articles use `min(100% - 80px, 820px)`. At 800px both gain 20px side gutters. Main spacing tokens are recorded above; sections additionally use deliberate larger intervals rather than a uniform card grid.

The exhibition hero pairs text and image in a .92fr/1.08fr grid with a 48px gap. At 800px it stacks, retaining text, actions and prerequisites before the image. Benefit rows shift from three columns to two at 800px and one at 540px. Setup panels stack at 800px. Support uses a sticky 230px topic rail, narrows it to 170px at 800px and becomes a single column at 540px. The guide feature stacks at 540px. Tables have a horizontal overflow wrapper.

The white sticky header is 88px tall, then 76px at 800px. Navigation stays visible: the setup shortcut is removed at 800px and the extra download shortcut at 540px. Scroll padding and section margins clear the header. Retain the skip link.

## Elevation & Depth

The site is predominantly flat: full-color fields, white surfaces and fine rules establish separation. The genuine product capture alone receives a dark device frame and a soft shadow (`0 28px 60px #00000030`); it is an exhibit, not a general card treatment.

**The Real Evidence Rule.** Use genuine product captures with their provenance retained; do not invent remote sessions or product UI.

## Shapes

Controls have modest corners; bounded workbench and help surfaces use the surface radius from the frontmatter. Device imagery uses a 22px outer frame and 14px image corners, reduced to 13px/8px on phones. The frame padding reduces from 9px to 5px. App identity and App Store badge retain their own silhouettes. FAQ and benefit rows remain open, ruled structures rather than enclosed cards.

## Components

### Buttons

Direct, solid controls. Shared buttons have a 52px minimum height, 600 weight and 1.4 line-height. Primary, light and outline variants use the frontmatter tokens. The outline has a current-color border; light and outline hover use sky, with deep blue text. Text links and navigation links have a 44px minimum height. Preserve the genuine App Store badge for the acquisition action.

### Navigation

White sticky navigation uses compact sentence-case links with 6px corners, sky hover/current-page fill and deep blue text. The dark download shortcut changes to blue on hover. Current pages use `aria-current`. Footer and breadcrumb links retain generous interactive height.

### Cards / Containers

The white setup workbench is the canonical bounded surface: 36px padding reduces to 25px at 800px and 20px at 540px. Sky help and guide callouts sit directly on white; article prose stays unenclosed. Use the surface radius without ambient card shadows.

### Inputs / Fields

The FAQ uses a labeled native search input with a white fill, a fine slate border (`#97a5bb`), control corners and blue caret. Search progressively appears with JavaScript, filters answer text, opens matches, announces counts through a polite live region and offers Clear. Zero matches show a quiet paper panel. Native `details`/`summary` disclosures remain usable without JavaScript; blue chevrons reverse on opening.

### Platform selector

Native buttons become an ARIA tablist only when enhanced. Tabs have 48px minimum height, paper fill at rest and blue/white selection. Left/Right cycle, Home/End select the ends, and only the active tab enters the normal tab sequence. Panels are focusable and labeled. Without JavaScript, all setup paths remain readable. The thin arrow rail communicates the network path, with no simulated connection status.

### Focus and motion

Interactive focus is a 3px blue outline with 5px offset; blue exhibition/download fields use white outlines. All buttons, links, summaries and inputs use manipulation touch behavior. The product image arrives once over 850ms with `cubic-bezier(.16, 1, .3, 1)`, translating 24px upward and restoring saturation. Color transitions use 160ms ease-out. These effects exist only under `prefers-reduced-motion: no-preference`; default content remains visible.

## Do's and Don'ts

### Do:
- Do preserve the app identity, genuine screenshots and their provenance.
- Do use white reading surfaces and muted text with navy headings for longer help content.
- Do retain visible focus, native disclosure behavior and keyboard navigation when extending components.
- Do keep the self-hosted font and its OFL license together.

### Don't:
- Don't introduce glass, decorative glows or numbered feature tiles into this world.
- Don't replace real app evidence with invented screenshots.
- Don't turn the informational connection rail into an implied live connection state.
- Don't animate when the visitor requests reduced motion.
