Apple India-Inspired Website --- UI/UX Design Specification
Document: design.md
Reference: https://www.apple.com/in/\
Prepared: 19 October 2026
Purpose: A practical design contract for product designers,
frontend engineers, content designers, and QA.
Status: Synthesized from the four supplied research/specification
files. Reference-derived patterns are separated from implementation
recommendations.

1. Executive summary
Apple India is best understood as a photography-first storefront that
behaves like a gallery before it behaves like a shop. The interface is
intentionally quiet: neutral chrome, concise copy, large product
imagery, a small action-blue palette, and repeatable purchase/support
paths. The site combines two modes:
- Showcase: low-density, cinematic, emotionally engaging product
  stories.
- Utility: compact navigation, search, shopping bag, buying
  information, disclosures, and a dense but well-organized footer.
The design system should preserve the rhythm and interaction logic of
the reference without treating campaign content, exact measurements, or
Apple-owned assets as reusable generic defaults. Homepage products,
promotions, and campaign order change over time; the durable pattern is
the hierarchy, not a fixed list of products.
Design outcome
Create a premium, clear, responsive commerce experience where users can
understand a featured product quickly, browse categories in one step,
discover relevant offers, and continue to product details or purchase
without ambiguity.
Confidence labels
- Observed/reference pattern: described consistently across the
  supplied research files.
- Implementation token: a recommended starting value inferred from
  the reference, not a claim about Apple's private source CSS.
- Validate: must be checked against current screenshots, real
  content, and the implementation's own requirements before
  pixel-level sign-off.
This is an independent reference-derived specification, not an official
Apple design document.
2. Product and UX principles
1. One idea per module. Each hero or tile communicates one product,
   benefit, or campaign.
2. The product is the layout. Photography should carry the visual
   weight; do not put every product in a floating, shadowed card.
3. Quiet chrome. Navigation and controls remain legible but
   visually secondary to the campaign.
4. Short, confident copy. Use concise headlines, one short
   supporting line, and at most two actions in a module.
5. Blue means interaction. Reserve action blue for links, focus
   indicators, and primary actions; do not use it as decoration.
6. Whitespace creates hierarchy. Prefer spacing and scale to
   borders, gradients, and shadows.
7. Predictable behavior. Keep navigation, action styling, search,
   and footer conventions consistent.
8. Progressive disclosure. Keep campaign copy concise while making
   eligibility, financing terms, and legal details easy to reach.
9. Responsive art direction. Change crops and text placement for
   mobile rather than merely shrinking desktop layouts.
10. Accessibility and performance are design requirements. Keyboard
    support, reduced motion, stable image dimensions, and fast first
    render are part of the intended experience.
11. Local relevance without a separate visual language. Use
    India-specific currency, date formats, support details, and verified
    offer terms within the same neutral system.
12. Truth over persuasion. Never invent discounts, urgency, reviews,
    stock availability, product specifications, or financing terms.
Avoid
- Decorative gradients or glass effects unrelated to readability or
  actual interface material.
- Multiple accent colors competing with the product.
- Long paragraphs, several headlines, or more than two CTAs inside a
  hero.
- Generic stock photography, distorted product imagery, or
  inconsistent crops.
- Heavy card shadows, arbitrary borders, and excessive corner rounding
  on full-width campaign tiles.
- Autoplaying sound, unpausable animation, fake scarcity, and
  placeholder links in production.
- Reusing Apple logos, product renders, campaign artwork, films, or
  proprietary font files without appropriate rights.
3. Audience, goals, and success criteria
Primary audiences
- Intent-led shoppers: know the category or product and want a
  short route to buying.
- Explorers: browse product families, benefits, comparisons, and
  editorial stories.
- Existing customers: need support, account, order, store, or
  service destinations.
- India-focused shoppers: need clear, accurate information about ₹
  pricing, eligible-card offers, No Cost EMI, trade-in, delivery, and
  pickup.
- Education and business customers: need access to relevant
  purchasing routes without overcrowding the primary navigation.
Core journeys
  User goal               Entry point             Desired next step
  Learn about a featured  Hero or promo tile      Product overview
  product                                         

  Buy or pre-order        Hero/tile CTA           Correct product
                                                  configuration or
                                                  purchase flow

  Browse a category       Global navigation or    Category landing page
                          menu                    

  Check financing or      Offer ribbon / buying   Eligibility and terms
  promotions              information             

  Find support or order   Navigation/footer       Relevant support
  status                                          destination

  Find a store            Footer/store link       Store locator

  Browse entertainment    Media gallery           Selected title or
                                              service destination
Suggested success measures
- Hero and tile CTA click-through rate.
- Search engagement and search-to-product click-through.
- Category navigation success and time to destination.
- Offer-information engagement and reduced confusion around
  eligibility.
- Mobile menu completion and first meaningful interaction.
- Core Web Vitals targets: LCP ≤ 2.5 seconds, INP ≤ 200 ms, CLS ≤ 0.1
  where practical.
- Accessibility defect count, broken-link count, and
  horizontal-overflow count.
These are suggested measurement targets, not claims about Apple's
internal analytics.
4. Information architecture
4.1 Global navigation
Reference order:
1. Brand/home mark
2. Store
3. Mac
4. iPad
5. iPhone
6. Watch
7. AirPods
8. Home
9. Entertainment
10. Accessories
11. Support
12. Search
13. Shopping bag
For a different product, replace the reference categories with the
actual site's categories. Keep the primary row short; move long-tail
destinations into category menus and the footer.
4.2 Navigation behavior
Desktop - Compact horizontal bar, aligned to a common baseline. -
Brand mark at the start, categories distributed through the center,
search and bag at the end. - Category flyouts may organize links into
Explore, Shop, and More from \(category\). - Flyouts must
have clear open/close behavior and not obscure the page without a
dismissible path. - The global navigation remains above page content in
the stacking order.

Compact/tablet/mobile - Replace the word-link row with a clearly
labeled Menu control when the full navigation no longer fits. - Keep the
brand/home, search, and bag reachable. - Use a full-screen or large
overlay/drawer with readable, left-aligned links. - Prevent background
scrolling while the menu is open. - Close using an explicit close
control and Escape where supported; return focus to the menu trigger. -
Avoid hover-only navigation. Every menu must work with keyboard and
touch.

Recommended responsive thresholds (starting points) - Small:
max-width: 734px - Compact navigation: max-width: 833px - Medium:
735px–1068px - Large: 1069px–1439px - Extra-large: 1440px+

Treat these as reference-derived starting points. Test actual content at
320, 375, 390, 734, 768, 833, 1024, 1068, 1280, 1440, and wide desktop
sizes.
4.3 Homepage sequence
The supplied audit describes the following campaign sequence for the
audited date. The specific products, titles, and offers are
time-sensitive; use this as an example of page rhythm, not as
permanent content.
1. Global navigation
2. Optional India-specific offer ribbon
3. Primary full-bleed hero
4. Secondary campaign/festive hero
5. Third hero or cinematic feature
6. Product promotion tiles, generally in balanced pairs
7. Additional product/service promotions
8. Horizontal entertainment/editorial gallery
9. Footnotes and legal disclosures
10. Footer directory
11. Region, copyright, and legal base row
The rhythm alternates large, low-density stories with smaller
product/service promotions. Do not turn every section into an identical
card.
4.4 Footer information architecture
Recommended groupings drawn from the reference:
- Shop and Learn
- Wallet and payments
- Account
- Entertainment and services
- Apple Store / physical retail / buying support
- Business
- Education
- Healthcare
- Government
- Values
- About
- Legal, privacy, region, and site map
Include a clear store-finder/help strip above the directory when
relevant. On mobile, collapse groups into accessible accordions. Keep
legal text and country/region controls reachable without excessive
scrolling.
5. Visual design foundations
5.1 Color tokens
The reference is largely monochrome. Product and campaign photography
supplies most of the color; UI color is restrained.
  Token                       Suggested value               Purpose
  --color-canvas            #FFFFFF                     Main page background

  --color-canvas-subtle     #F5F5F7                     Offer ribbon, subtle
                                                            surfaces, footer

  --color-canvas-elevated   #FAFAFC                     Light flyout/search
                                                            surface

  --color-ink               #1D1D1F                     Primary text

  --color-ink-secondary     #333336                     Secondary UI text

  --color-ink-tertiary      #6E6E73                     Supporting text

  --color-ink-quaternary    #86868B                     Metadata and fine
                                                            print; verify contrast

  --color-white             #FFFFFF                     Text/icons on dark
                                                            imagery

  --color-black             #000000                     Pure black media
                                                            backgrounds where
                                                            appropriate

  --color-link              #0066CC                     Text links on light
                                                            surfaces

  --color-link-dark         #2997FF                     Links on dark surfaces

  --color-action            #0071E3                     Primary action and
                                                            focus ring

  --color-action-hover      #0076DF                     Hover state

  --color-action-active     #006EDB                     Pressed state

  --color-divider           rgba(0, 0, 0, 0.16)         Quiet rules and
                                                            separators

  --color-divider-dark      rgba(255, 255, 255, 0.24)   Separators on dark
                                                            surfaces

  --color-success           #008009                     Commerce success
                                                            feedback only

  --color-warning           #B64400                     Warning feedback only

  --color-danger            #E30000                     Destructive/error
                                                        feedback only
Color rules - Keep the interface neutral; do not sample product
finishes or campaign artwork into UI tokens. - Blue communicates an
available action, not decoration. - Use semantic colors only for
meaningful status feedback. - Every light/dark component variant must
update text, links, focus treatment, and scrim together. - Validate
contrast on the actual background and image crop. Do not assume a color
is accessible because it is used in the reference.
5.2 Typography
Use the system sans-serif stack unless the project is licensed to use
the intended typeface. Apple's SF Pro is proprietary; do not bundle or
redistribute it without rights.
font-family: "SF Pro Display", "SF Pro Text", "Helvetica Neue",
  Helvetica, Arial, sans-serif;
A safe general-purpose fallback is:
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
Use display styling for large marketing headlines and text styling for
navigation, body, controls, and footer. Limit most modules to regular
400 and semibold 600 weights.
  Role               Large desktop         Medium   Small/mobile         Weight
  Hero/tile            56px / 1.07    48px / 1.08   32px / 1.125            600
  headline                                                       

  Chapter/display         48--56px       40--48px       32--40px            600
  headline                                                       

  Promo headline       40px / 1.10   32px / 1.125   32px / 1.125            600

  Hero subhead         28px / 1.14    24px / 1.17    19px / 1.21            400

  Body copy            17px / 1.47    17px / 1.47     16--17px /            400
                                                            1.45 

  Navigation            12px / 1.4     12px / 1.4 28px / 1.14 in        400/600
                                                   expanded menu 

  Button               14px / 1.29    14px / 1.29       14--17px            400

  Footer / footnote    12px / 1.33    12px / 1.33     12px / 1.4  400; headings
                                                                        600
These are practical starting values synthesized from the more detailed
supplied audit. Tune by screenshot and content fit.

Typography rules - Keep headlines short and sentence case;
punctuation is allowed when it supports the brand voice. - Limit hero
headlines to two lines at common viewport widths where possible. - Do
not use all caps for long marketing headlines. - Avoid arbitrary letter
spacing, especially positive tracking on display text. - Use clear
hierarchy through size and weight rather than multiple colors. - For
Hindi or other Indic content, use an appropriate script-capable font and
test line-height, shaping, and mixed-script behavior.
5.3 Layout and grid
- Full-bleed heroes span the viewport.
- Promo tiles use a 12px gutter and are generally paired on
  desktop/tablet; stack on small screens.
- The footer directory and constrained text content may use a centered
  max-width container around 980--1200px.
- Overall page width should be fluid, not locked to one narrow
  container.
- Suggested desktop gutters: 20--24px between grid columns; mobile
  page margins: 16--22px.
- Suggested grid: 12 columns desktop, 8 tablet, 4 mobile.
- Reserve media dimensions with width/height or aspect-ratio to
  prevent layout shift.
5.4 Spacing scale
Use a 4px base scale and reuse values before introducing new ones.

  Token            Value
  --space-1        4px
  --space-2        8px
  --space-3       12px
  --space-4       16px
  --space-5       20px
  --space-6       24px
  --space-8       32px
  --space-10      40px
  --space-12      48px
  --space-14      56px
  --space-16      64px
  --space-20      80px
  --space-24      96px
  --space-30     120px

Typical relationships: - Headline to subhead: 8--12px. - Subhead to CTA
group: 17--24px. - CTA-to-CTA gap: 14--17px. - Hero top padding: about
48px; bottom padding: 56--60px on large screens. - Promo tile padding:
around 44--60px vertically, responsive to available height. - Between
major full-width modules: approximately 12px where the gallery rhythm
calls for it.
5.5 Radius, borders, and elevation
- Marketing CTA buttons: capsule/pill radius (999px).
- Homepage hero and promo tiles: square corners; the gutter separates
  tiles.
- Functional controls: use consistent, restrained radii (8--12px as a
  starting point).
- Borders: quiet 1px separators where needed, not around every tile.
- Avoid drop shadows on campaign tiles and the global nav.
- Use translucent blur only for the global navigation material if it
  improves the intended visual layering; provide an opaque fallback.
- Do not use glass, gradients, or shadows as general decoration.
5.6 Iconography
- Use simple, consistent, monoline icons.
- Keep icon sizes around 16--20px in compact navigation and 24px in
  large mobile menus.
- Icon-only controls require accessible names.
- Avoid emoji and multi-color decorative iconography in core site
  chrome.
- Use a consistent icon set rather than mixing visual styles.
6. Component specifications
6.1 Global navigation
Anatomy: brand/home link, category links or Menu, search, shopping
bag.

Starting dimensions - Desktop: approximately 44px tall. - Compact
navigation: approximately 48px tall. - Safe-area aware padding on
supported mobile devices. - High stacking priority so page content
cannot cover the navigation.

States - Default, hover, focus-visible, current destination, menu
open, search open, bag open. - Hover may increase text contrast; do not
rely on hover to reveal essential content. - Focus indicator must remain
visible against translucent backgrounds.

Behavior - Logo returns to home. - Search and bag have clear
accessible labels. - Menus open and close consistently, and Escape
closes overlays where appropriate. - When a flyout is open, background
content is visually subdued without making the menu feel like a
disconnected floating card. - Avoid a visible bottom border on the
homepage header if the translucent material already creates sufficient
separation.
6.2 Announcement / offer ribbon
Purpose: communicate one time-sensitive promotion or service update.
- Full-width, subtle light-gray surface.
- Centered concise text with one inline destination.
- Use India-specific currency and only verified offer terms.
- Use footnote markers for conditions and map them to a readable
  disclosure.
- Allow clean wrapping on narrow screens.
- If no valid offer exists, remove the ribbon rather than showing an
  empty placeholder.
- Do not add a carousel or fake urgency to the ribbon.
6.3 Campaign hero
Anatomy 1. Optional eyebrow/product label 2. Headline 3. Short
supporting line or availability date 4. One or two actions 5. Image or
video media

Layout variants - Centered, text above product. - Dark, light, or
campaign-art theme. - Full-bleed cinematic hero. - Split layout only
when content genuinely benefits from separate text and image columns.

Starting dimensions - Large desktop: min-height around 580px; up to
about 690px for tall storytelling moments. - Medium: around 570--650px
depending on content. - Small: min-height around 500px. - Do not default
to 100vh; browser chrome can crop the image on mobile.

Rules - Place text in the quiet part of the image, usually above the
product. - Keep the product visually dominant without colliding with
copy or CTAs. - Use art-directed small, medium, and large crops; mobile
is not just a scaled desktop image. - Use a static poster/start frame
before any optional animation. - For text over imagery, test contrast at
every breakpoint and add a restrained scrim only when necessary. - Use a
meaningful image alt description for product details; avoid repeating
the headline in alt text.
6.4 Product and campaign tiles
- Desktop/medium: two-column grid, approximately 12px gap.
- Small screens: one column and edge-to-edge tiles where the reference
  pattern calls for it.
- Keep pairs visually balanced; do not leave a lone half-width tile
  unless intentionally designed.
- Suggested minimum heights: around 580px large, 490px medium, 500px
  small; validate with actual content and media.
- One headline, optional subhead/callout, and at most two actions.
- Use original art direction per product.
- When two actions exist, each action is its own target; avoid making
  the entire image a third ambiguous link.
- Clip media to the tile boundary so it does not spill into the
  gutter.
6.5 Links and buttons
Text links - Blue on light backgrounds; lighter blue on dark
backgrounds. - Concise verbs: "Learn more", "Shop", "Buy", "Compare",
"Explore". - Hover/focus must be visible without depending on color
alone.

Primary transactional button - Use for high-priority actions such as
Add to bag, Continue, or checkout. - Blue filled capsule with white
label. - Include hover, active, focus-visible, loading, and disabled
states when applicable.

Secondary action - Usually text link or a restrained
outlined/neutral variant, depending on context. - Must be
distinguishable from body copy. - Do not turn every link into a filled
button.

Interaction - All actions must have real destinations or real
behavior. - Use adequate touch targets (aim for at least 44×44 CSS px
where feasible). - Avoid nested interactive elements and duplicate click
targets.
6.6 Search overlay
Required states: - Closed - Open and focused - Query entered - Loading -
Results - No results - Error - Cleared query

Behavior: - Provide a visible input label or accessible name. - Support
keyboard submit, clear, and close. - Keep focus within the overlay while
it is modal; restore focus to the trigger on close. - Show useful empty
and error states. - Do not show fabricated suggestions or results. -
Search result destinations must be valid.
6.7 Shopping bag / cart
Required states: - Empty bag - Items present - Updating quantity -
Removing item - Loading - Error - Checkout transition

Behavior: - Display accurate item counts and totals. - Make
remove/update actions explicit and reversible where practical. - Keep
item price, selected options, quantity, and totals legible. - Provide a
clear path to continue shopping and checkout. - Never simulate
successful payment or inventory state without backend confirmation.
6.8 Entertainment/editorial carousel
- Horizontal media cards with snap points and clear visual grouping.
- Use high-quality, correctly licensed poster art.
- Provide a title, genre/eyebrow where appropriate, one short line,
  and one clear action.
- Support touch swiping, keyboard navigation, and visible controls
  where needed.
- Do not autoplay sound.
- Respect reduced motion and avoid trapping keyboard focus.
- If scroll position or pagination is shown, expose it accessibly.
6.9 Footnotes and disclosures
- Mark offer claims, availability dates, and conditions at the point
  of use.
- Provide matching, readable disclosures near the footer or in the
  relevant purchase context.
- Use semantic links between marker and disclosure where possible.
- Do not make legal copy so small or low-contrast that it becomes
  unusable.
- Claims about cashback, EMI, trade-in, warranties, or availability
  must be verified and dated.
6.10 Footer
- Use a subtle neutral surface and a constrained content width.
- Group links by user intent and label each group clearly.
- Use a multi-column directory on desktop and accordions on mobile.
- Include store locator, contact, regional selector, copyright,
  privacy, terms, sales/legal, and site map as appropriate.
- Use semantic navigation landmarks and accessible accordion controls.
- Avoid duplicating the full primary nav if it adds no value; the
  footer serves long-tail discovery.
7. Content design and localization
Voice
- Clear, concise, confident, human, benefit-led.
- Short spoken phrases and sentence case.
- Avoid overstatement, exclamation-heavy copy, and jargon.
- Use one main message per section.
Copy patterns
Good pattern - Headline: one product idea or benefit. - Supporting
line: one short explanation, availability date, or context. - CTA:
direct verb. - Disclosure: concise marker and complete, readable terms.

Avoid - Multiple headlines in one tile. - Generic "Click here". -
Unsupported superlatives. - Fake urgency ("last chance") without
verified conditions. - Marketing copy copied verbatim from Apple when
creating a different brand.
India localization
- Use ₹ for rupee amounts and en-IN conventions.
- Use "No Cost EMI" when that is the verified offer wording; do not
  silently change it to "interest-free".
- Format phone numbers and dates for India.
- Confirm local availability, taxes, bank eligibility, tenure,
  exclusions, and offer caps before publishing.
- Ensure every footnote marker maps to the correct terms.
- For Hindi or bilingual pages, use proper Indic fonts and test line
  wrapping, punctuation, and screen-reader pronunciation.
8. Motion and interaction
Motion should explain state changes, provide feedback, or support
storytelling. It should not be ornamental.

Suggested tokens:
:root {
  --motion-fast: 150ms;
  --motion-normal: 240ms;
  --motion-slow: 320ms;
  --ease-standard: cubic-bezier(0.28, 0.11, 0.32, 1);
}
- Use short opacity/transform transitions for menus and overlays.
- Avoid large parallax shifts and unnecessary scroll-linked effects.
- Avoid animating layout-heavy properties when transform/opacity can
  achieve the same result.
- Provide poster imagery and user control for moving media.
- Do not autoplay audio.
- Respect prefers-reduced-motion: reduce; remove non-essential
  motion and avoid automatic carousel movement.
- Animation must not delay navigation or hide important content.
- Make open/closed states understandable without animation.
9. Responsive behavior
Small screens (≤ 734px)
- Single-column campaign tile layout.
- Compact navigation.
- Hero and promo copy must fit without clipping or overlap.
- Use mobile-specific image crops and appropriate text positioning.
- Preserve clear CTA separation and comfortable touch targets.
- Footer groups become accordions.
- Avoid horizontal overflow at 320px width.
Compact navigation range (≤ 833px)
- Collapse the desktop word-link row into Menu before it becomes
  crowded.
- Keep brand, search, and bag reachable.
- Use safe-area-aware padding and avoid covering content with
  overlays.
Medium screens (735--1068px)
- Use two-column promo layouts only when the copy and imagery remain
  legible.
- Reduce type and padding before reducing contrast or hierarchy.
- Check landscape tablets and short viewport heights.
Large screens (≥ 1069px)
- Use paired promo tiles with consistent gutters.
- Use large art-directed product images and balanced negative space.
- Do not allow text columns to become excessively wide.
- Preserve full-bleed campaign imagery.
Responsive test matrix
Test at 320, 375, 390, 734, 768, 833, 1024, 1068, 1280, 1440, and 1920px
widths; also test short-height landscape layouts, browser zoom to 200%,
and device safe areas.
10. Accessibility requirements
Target WCAG 2.2 AA as the implementation baseline.
- Use semantic landmarks (header, nav, main, footer) and a
  logical heading order.
- Provide skip navigation where useful.
- All controls must be keyboard reachable and have visible focus.
- Use accessible names for icon-only buttons.
- Ensure overlays and menus support keyboard interaction, Escape where
  appropriate, focus management, and focus restoration.
- Aim for at least 4.5:1 contrast for normal text and 3:1 for large
  text and meaningful UI boundaries, subject to WCAG exceptions.
- Never communicate status through color alone.
- Provide descriptive alt text for informative images and empty alt
  for decorative imagery.
- Use captions/transcripts where video content requires them.
- Respect reduced motion, zoom, text resizing, and reflow.
- Label form controls and provide clear, actionable validation
  messages.
- Ensure carousel controls have understandable names and do not make
  keyboard navigation confusing.
- Test with keyboard-only navigation and at least one screen reader.
11. Imagery, media, and performance
Imagery
- Use high-resolution, professionally art-directed product or campaign
  photography.
- Keep product proportions and colors accurate.
- Use negative space intentionally for text placement.
- Supply small, medium, and large art-directed crops; use
  srcset/sizes where appropriate.
- Set explicit dimensions or aspect-ratio.
- Use AVIF/WebP where supported with a suitable fallback.
- Never hotlink production Apple assets for a new implementation; use
  original or properly licensed material.
Loading and runtime
- Prioritize the main hero image and avoid lazy-loading the LCP image
  if that delays its appearance.
- Lazy-load below-the-fold images.
- Defer non-critical media and scripts.
- Prevent layout shift by reserving media space.
- Use responsive image sizes instead of sending desktop originals to
  phones.
- Avoid expensive blur, filter, and scroll effects on large surfaces.
- Keep the interface usable while optional animation or media loads.
- Measure real Core Web Vitals rather than assuming the page is fast.
12. Suggested design tokens (CSS)
The values below are a starting implementation contract, synthesized
from the supplied specifications. Validate them against the target page
and project.
:root {
  /* Color */
  --color-canvas: #ffffff;
  --color-canvas-subtle: #f5f5f7;
  --color-canvas-elevated: #fafafc;
  --color-ink: #1d1d1f;
  --color-ink-secondary: #333336;
  --color-ink-tertiary: #6e6e73;
  --color-ink-quaternary: #86868b;
  --color-black: #000000;
  --color-white: #ffffff;
  --color-link: #0066cc;
  --color-link-on-dark: #2997ff;
  --color-action: #0071e3;
  --color-action-hover: #0076df;
  --color-action-active: #006edb;
  --color-divider: rgba(0, 0, 0, 0.16);
  --color-divider-dark: rgba(255, 255, 255, 0.24);

  /* Typography */
  --font-display: "SF Pro Display", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-text: "SF Pro Text", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-fallback: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-weight-regular: 400;
  --font-weight-semibold: 600;
  --type-hero: clamp(2rem, 4vw, 3.5rem);
  --type-body: 1.0625rem;
  --type-small: 0.75rem;

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-14: 56px;
  --space-16: 64px;
  --space-20: 80px;
  --space-24: 96px;

  /* Layout */
  --page-gutter: clamp(16px, 3vw, 48px);
  --content-max: 1200px;
  --tile-gutter: 12px;
  --nav-height: 44px;
  --nav-height-compact: 48px;

  /* Shape */
  --radius-none: 0;
  --radius-control: 8px;
  --radius-control-large: 12px;
  --radius-pill: 999px;

  /* Motion */
  --motion-fast: 150ms;
  --motion-normal: 240ms;
  --motion-slow: 320ms;
  --ease-standard: cubic-bezier(0.28, 0.11, 0.32, 1);
}
Navigation material (optional)
.global-nav {
  background: rgba(250, 250, 252, 0.8);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  backdrop-filter: saturate(180%) blur(20px);
}

@supports not ((backdrop-filter: blur(20px))) {
  .global-nav {
    background: rgba(250, 250, 252, 0.92);
  }
}
Do not apply the blur treatment to every card or section. It belongs
only where the navigation material needs to sit above content.
13. Suggested component architecture
Use the project's existing framework and styling approach. The component
names below are recommendations, not mandatory abstractions.
- SiteHeader
- GlobalNavigation
- DesktopCategoryMenu
- MobileNavigation
- AnnouncementBar
- CampaignHero
- ProductPromoTile
- PromoGrid
- ProductFeatureSection
- MediaCarousel
- TextLink
- PrimaryAction
- SearchOverlay
- ShoppingBagPanel
- FootnoteList
- SiteFooter
- FooterAccordion
Component API guidance
- Separate campaign/product content data from presentation where
  practical.
- Prefer tokens over repeated hard-coded styles.
- Use explicit variants such as light, dark, centered,
  fullBleed, and split.
- Avoid a single inflexible component that tries to handle every
  visually different campaign.
- Document exceptions when a campaign genuinely needs custom art
  direction.
- Keep interactions functional and testable; avoid decorative controls
  that look interactive but do nothing.
14. Primary workflow specifications
14.1 Product discovery to purchase
1. User enters from the homepage, category navigation, or search.
2. User reviews the product overview and key benefits.
3. User compares available configurations and understands the price.
4. User reviews trade-in/financing options when applicable.
5. User chooses delivery or pickup when supported.
6. User reviews the final order summary and proceeds to checkout.
Every transition should preserve the selected product and configuration.
Pricing and offer terms must come from a trusted data source.
14.2 Offer discovery
1. User sees a concise offer ribbon or product-level offer callout.
2. User opens the offer details.
3. User can identify eligibility, participating cards, tenure, caps,
   exclusions, and dates.
4. User returns to the product or purchase flow without losing context.
14.3 Support/store discovery
1. User opens Support or the footer.
2. User selects a relevant help topic or store finder.
3. Destination is valid and works on mobile.
4. If a destination is unavailable, provide a clear explanation and an
   alternate path.
15. QA and definition of done
Visual quality
- [ ] Page hierarchy reads correctly at a glance.
- [ ] Product imagery is high quality, correctly cropped, and not
  distorted.
- [ ] Headlines, supporting copy, and CTAs align consistently.
- [ ] Color, typography, spacing, and button styles use documented
  tokens.
- [ ] Light and dark themes preserve legibility.
- [ ] No unnecessary shadows, borders, gradients, or card rounding
  have been introduced.
Responsive quality
- [ ] Tested at 320, 375, 390, 734, 768, 833, 1024, 1068, 1280, 1440,
  and 1920px.
- [ ] No horizontal overflow.
- [ ] Menus, search, bag, carousels, and footer work with touch.
- [ ] Hero text and actions do not overlap important imagery.
- [ ] Mobile crops are intentionally art-directed.
- [ ] Safe-area insets and landscape layouts are handled.
Accessibility
- [ ] Keyboard focus is visible and logical.
- [ ] Icon-only controls have accessible names.
- [ ] Headings and landmarks are semantic.
- [ ] Contrast is checked on actual backgrounds and images.
- [ ] Reduced motion is respected.
- [ ] Overlays manage and restore focus correctly.
- [ ] Form errors are clear and associated with fields.
- [ ] Screen-reader and keyboard spot checks are complete.
Performance
- [ ] Main hero media is prioritized.
- [ ] Below-the-fold media is lazy-loaded appropriately.
- [ ] Images are responsive and compressed.
- [ ] Media dimensions prevent layout shifts.
- [ ] No unnecessary blocking scripts or heavy animation.
- [ ] Core Web Vitals have been measured.
Functional integrity
- [ ] Every CTA has a real destination or action.
- [ ] Search handles loading, results, empty, clear, and error states.
- [ ] Bag/cart count and totals are accurate.
- [ ] No placeholder links or fake offer claims remain.
- [ ] No new console errors or failed critical network requests.
- [ ] Purchase and offer information is sourced from current trusted
  data.
16. Reference interpretation and limitations
This specification synthesizes four supplied files: 1. A
reverse-engineered Apple India homepage and UX specification. 2. A
broader Apple Store India platform/navigation and commerce
specification. 3. A detailed as-shipped design-system audit emphasizing
exact navigation behavior, color tokens, typography, spacing, and
current campaign rhythm. 4. An implementation-oriented Apple-inspired
design system with component, responsive, accessibility, and QA
guidance.
Reconciliation decisions
- Where the files differed, the more detailed system audit was
  preferred for the design's signature behaviors: 12px tile gutters,
  square promo tiles, restrained/no tile shadows, compact nav at
  833px, and campaign-first hierarchy.
- Typography sizes and hero heights are documented as starting
  points, not guaranteed internal Apple values.
- Campaign products, dates, streaming titles, offer amounts, and page
  sequence are time-sensitive and should not be hard-coded as
  permanent requirements.
- Accessibility requirements are written as the implementation target,
  not a claim that every reference behavior has been independently
  audited against every WCAG criterion.
- This document describes public-facing patterns. It does not expose
  or claim access to Apple's private design files or source CSS.
Official reference links
- Apple India: https://www.apple.com/in/
- Apple Human Interface Guidelines --- Foundations:
  https://developer.apple.com/design/human-interface-guidelines/foundations
- Apple Human Interface Guidelines --- Layout:
  https://developer.apple.com/design/human-interface-guidelines/layout
- Apple Developer Design: https://developer.apple.com/design/
Final direction
Build the experience as a coherent system, not a collage of screenshots:
quiet navigation, neutral chrome, full-bleed product storytelling, short
benefit-led copy, clear blue actions, carefully art-directed responsive
imagery, honest India-specific commerce disclosures, and a useful
footer. Validate every inferred measurement against current reference
screenshots and the actual product before production sign-off.