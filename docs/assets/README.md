# Spoor logos

The Spoor mark is a hoof print (a spoor) on a hexagon, in three colourways. Each
comes as an SVG (scalable, preferred) and a PNG (664 × 724/725 px). The orange is
`#F85840`, the same coral as the accent colour in the GUI and the exploration wiki.

| File | Looks like | Use it on |
|---|---|---|
| `Spoor_O_B.svg` / `.png` | Orange hexagon, black print | Dark backgrounds and small sizes, where the black hexagon would disappear: the GUI's top bar and browser-tab icon use this one. |
| `Spoor_B_O.svg` / `.png` | Black hexagon, orange print | Light backgrounds, where the black hexagon shows its shape: the GUI's top bar uses this one in day mode. |
| `Spoor_B_W.svg` / `.png` | Black hexagon, white print | Single-colour or monochrome use (print, stamps, anywhere colour isn't available). |

The local GUI (`spoor gui`) ships its own copies of `Spoor_O_B.svg` (night mode
and the browser tab) and `Spoor_B_O.svg` (day mode) at
`spoor/gui/assets/spoor-logo-night.svg` and `spoor-logo-day.svg`, because `docs/`
isn't part of the installed package. A test checks each copy is byte-identical to
its file here, so replace them together.
