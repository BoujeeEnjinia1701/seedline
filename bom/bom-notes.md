# BOM notes

- Costs are USD estimates for the TRL 3 paper design (SDL-CAL-001 section 11), not quotes. Supplier types are named for each line; no supplier has been chosen.
- Item numbers 1 to 14 match the callouts in `media/exploded.png`, the parts in `cad/src/model.py` and the component table in `docs/02-concept.md`. Items 15 and 16 have no callout.
- Item 6 is a set of six plates at about $1.25 each, assuming a printer is available. Plates weigh 40 to 54 g and print in 1.5 to 2.0 h each. Printer time and ownership are not costed.
- Item 2 is the base drive: a 15 T plate sprocket, a 15 T wheel sprocket (ratio 1.0), a 76-link chain and a spring idler. Item 16 is the optional ratio kit (SDL-DDR-002 item 4): the 12 and 18 T wheel sprockets and an offset link for the 74- and 77-link chains, which carry the ratio change decided in SDL-DDR-001 item 4.
- Item 12 is the decided bolted frame (SDL-DDR-001 item 8); the rails are 25 x 25 x 1.5 mm tube, sized in SDL-CAL-001 section 7.
- Item 13 uses 22 x 1.2 mm round tube (SDL-DDR-002 item 3; was 25 x 1.5 mm), which saves about 0.65 kg.
- Base seeder (items 1 to 13 and 15): $197.50, inside the about $200 replication target (SDL-REQ-001 R17) with a thin margin. With the row marker kit (item 14, $24.00) and the ratio kit (item 16, $16.00): $237.50, inside the $400 prototype budget in `project.yaml`.
- Mass (SDL-CAL-001 section 5): 13.9 kg base, 14.9 kg with the marker kit.
- Decided on 2026-10-02 (SDL-DEC-001), not yet in the BOM lines or prices: the housing door (line 5) is clear polycarbonate in a UV-stabilized grade; the housing gets a 13 mm slot with printed side liners for each plate thickness; the drive wheel (line 1) stays a steel disc wheel; no hopper window. USD 219.50 for the base seeder is accepted for the prototype, with the bronze bushing and go-kart kit savings to try at TRL 4.
