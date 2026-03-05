# Each region is a self-contained entry. Add new ones by copying the template.
# The app reads this file — changes take effect on reload.

REGIONS = [
    {
        "name": "Nile Delta, Egypt",
        "bbox": [29.5, 30.0, 32.0, 31.7],
        "zoom": 9,
        "wet": (10, 3),
        "dry": (5, 9),
        "ndvi": 0.20,
        "contrast": 0.25,
        "why": "Egypt banned most private groundwater wells in the Nile Valley, "
               "but illegal drilling has surged since 2010. Green fields outside "
               "official canal-irrigated zones are almost certainly pumping from "
               "the aquifer. The desert edge is the tell — nothing should be green there.",
        "what_to_look_for": [
            "Green patches at the desert margin (west and east edges of the delta)",
            "New irrigation appearing between years in Year-over-Year mode",
            "Fields green in dry season (May-Sep) that aren't near canals",
        ],
    },
    {
        "name": "Punjab, India-Pakistan",
        "bbox": [71, 28, 77, 33],
        "zoom": 7,
        "wet": (7, 9),
        "dry": (12, 2),
        "ndvi": 0.25,
        "contrast": 0.30,
        "why": "Punjab's aquifer is dropping 1 meter per year due to millions of "
               "tube wells pumping for rice and wheat. Free electricity subsidies "
               "encourage over-extraction. This is one of the fastest groundwater "
               "depletion zones on Earth.",
        "what_to_look_for": [
            "Near-total irrigation coverage — almost every field stays green in winter",
            "Year-over-year: expansion into previously fallow areas near the Thar Desert",
            "The India-Pakistan border is visible as different irrigation intensity",
        ],
    },
    {
        "name": "Central Valley, California",
        "bbox": [-121.5, 35, -119, 38],
        "zoom": 8,
        "wet": (12, 3),
        "dry": (6, 9),
        "ndvi": 0.25,
        "contrast": 0.30,
        "why": "California's 2014 SGMA law requires groundwater sustainability plans "
               "in overdrafted basins. Farmers who can't get surface water allocations "
               "drill deeper wells. Fields that stay green through summer drought are "
               "the ones pumping the most.",
        "what_to_look_for": [
            "Green orchards and fields in July-September when no rain falls",
            "Southern San Joaquin Valley has the most severe overdraft",
            "Year-over-year: fallowed fields (lost irrigation) show SGMA compliance",
        ],
    },
    {
        "name": "Aral Sea Basin, Central Asia",
        "bbox": [58, 39, 67, 44],
        "zoom": 7,
        "wet": (4, 6),
        "dry": (7, 9),
        "ndvi": 0.20,
        "contrast": 0.30,
        "why": "Soviet-era irrigation diversions from the Amu Darya and Syr Darya rivers "
               "shrank the Aral Sea by 90%. Uzbekistan's cotton fields are still irrigated "
               "from these rivers. The question: is irrigated area still expanding, or has "
               "the damage stabilized?",
        "what_to_look_for": [
            "Massive irrigated zones around Bukhara and the Fergana Valley",
            "The contrast between irrigated oases and surrounding desert",
            "Year-over-year: check if cotton land is expanding or contracting",
        ],
    },
    {
        "name": "Lake Naivasha, Kenya",
        "bbox": [36.2, -0.9, 36.5, -0.7],
        "zoom": 12,
        "wet": (3, 5),
        "dry": (7, 10),
        "ndvi": 0.20,
        "contrast": 0.25,
        "why": "Cut flower farms around Lake Naivasha supply European supermarkets "
               "and consume enormous amounts of water. The lake level has dropped "
               "significantly. Environmental groups have pushed for extraction limits, "
               "but farms keep expanding.",
        "what_to_look_for": [
            "Dense green rectangles (greenhouses and irrigated fields) around the lake shore",
            "Year-over-year: expansion of farm area into surrounding savanna",
            "Compare farm footprint to the lake's visible shoreline",
        ],
    },
]

# --- Template for adding new regions ---
# Copy this and fill in the fields:
#
# {
#     "name": "Region Name",
#     "bbox": [west_lon, south_lat, east_lon, north_lat],
#     "zoom": 8,
#     "wet": (start_month, end_month),
#     "dry": (start_month, end_month),
#     "ndvi": 0.25,
#     "contrast": 0.30,
#     "why": "Why this region matters for water governance...",
#     "what_to_look_for": [
#         "First thing to notice",
#         "Second thing to notice",
#     ],
# },
