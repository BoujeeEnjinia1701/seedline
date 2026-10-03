# BOM notes

- Costs are USD estimates for the TRL 3 paper design (SDL-CAL-001 section 11), not quotes. Supplier types are named for each line; no supplier has been chosen.
- Item numbers 1 to 14 match the callouts in `media/exploded.png`, the parts in `cad/src/model.py` and the component table in `docs/02-concept.md`. Items 15 and 16 have no callout.
- Item 5 includes two printed plate liners (about 57 g of PETG, USD 1.60) and the UV-stabilized grade of the clear 3 mm polycarbonate door (about USD 3.00 more than plain polycarbonate); the housing slot is 13 mm for the 6, 8 and 10 mm plates, with a thinner or no chain-side liner on the thicker plates.
- Item 6 is a set of six plates at about $1.25 each, assuming a printer is available. Plates weigh 40 to 54 g and print in 1.5 to 2.0 h each. Printer time and ownership are not costed.
- Item 2 is the base drive: a 15 T plate sprocket, a 15 T wheel sprocket (ratio 1.0), a 76-link chain and a spring idler. Item 16 is the optional ratio kit (SDL-DDR-002 item 4): the 12 and 18 T wheel sprockets and an offset link for the 74- and 77-link chains, which carry the ratio change decided in SDL-DDR-001 item 4.
- Item 12 is the decided bolted frame (SDL-DDR-001 item 8); the rails are 25 x 25 x 1.5 mm tube, sized in SDL-CAL-001 section 7.
- Item 13 uses 22 x 1.2 mm round tube (SDL-DDR-002 item 3; was 25 x 1.5 mm), which saves about 0.65 kg.
- Base seeder (items 1 to 13 and 15): $224.10, USD 24.10 over the about $200 replication target (SDL-REQ-001 R17); USD 219.50 of it was accepted for the prototype on 2026-10-02 and the liners and UV-stabilized door added $4.60. With the row marker kit (item 14, $24.00) and the ratio kit (item 16, $18.00): $266.10, USD 133.90 under the USD 400 value-engineering target (`budget_usd`, unchanged).
- Mass (SDL-CAL-001 section 5): 14.1 kg base, 14.9 kg with the marker kit.
- Decided on 2026-10-02 (SDL-DEC-001) and now in the BOM: the housing door (line 5) is UV-stabilized clear polycarbonate; the housing has a 13 mm slot with printed side liners; the drive wheel (line 1) stays a steel disc wheel; no hopper window. The bronze bushing and go-kart kit savings are to try at TRL 4 and are not in the prices.
