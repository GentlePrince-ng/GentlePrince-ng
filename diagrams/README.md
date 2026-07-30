# Diagrams

Hand-written SVG versions of the diagrams in the profile README. Vector, so they
scale to any size without blurring, and the text is real text — selectable,
searchable, and editable in any editor.

| File | Diagram |
| --- | --- |
| `1-data-estate.svg` | Sources → ingest → model → serve |
| `2-icl-study-design.svg` | ICL: design fixed before collection, instruments, field QA, outputs |
| `3-phc-data-explorer.svg` | PHC Data Explorer pipeline with the supervised AI branch |
| `4-glide-quality-gate.svg` | GLIDE: 16-rule engine and the human validation gate |
| `5-geospatial-rules.svg` | Geopoint parsing, accuracy threshold, grid-snap duplicate detection |
| `6-ga4-three-era-reconciliation.svg` | Three measurement eras into one article-level table |

All 1600 × 900 (16:9), so they drop straight into slides.

## Why the profile README still uses Mermaid

These SVGs have a white background, which reads as a bright slab against
GitHub's dark theme. Mermaid re-themes itself to match the reader, so it stays
in the README. These files are for everywhere Mermaid doesn't reach — slide
decks, a CV, LinkedIn, PDFs, print.

## Palette

| Role | Hex |
| --- | --- |
| Text and connectors | `#334155` |
| Process nodes | `#2E8B74` |
| Decision diamonds | `#D98A2B` |
| Data stores | `#F1F5F9` fill, `#CBD5E1` border |
| Flagged / rejected paths only | `#B4483C` |
| Pending, not rejected | `#64748B` |

Type is Inter with a Helvetica and Arial fallback. When an SVG is loaded as an
image the browser won't fetch a webfont, so the fallback is what actually
renders — which is why the stack matters.

## Converting

```bash
# PNG at 2x for slides
inkscape 1-data-estate.svg --export-type=png --export-width=3200

# PDF for print
inkscape 1-data-estate.svg --export-type=pdf
```

Or open in a browser and print to PDF — vector output, no extra tooling.
