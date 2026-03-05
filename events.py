# Curated groundwater and irrigation events with sources.
# Add new entries at the top of each region's list.
# The app displays these in a browsable sidebar panel.

EVENTS = {
    "Nile Delta, Egypt": [
        {
            "year": 2024,
            "title": "Egypt tightens penalties for illegal well drilling",
            "summary": "New amendments to Water Resources Law 147 impose prison terms "
                       "and fines up to EGP 500,000 for unauthorized groundwater extraction. "
                       "Satellite monitoring cited as an enforcement tool.",
            "url": "https://www.al-monitor.com/originals/2024/02/egypt-cracks-down-illegal-wells",
        },
        {
            "year": 2023,
            "title": "Groundwater depletion threatens Egypt's food security",
            "summary": "A Nature study found the Nile Delta aquifer is being depleted "
                       "faster than it recharges, driven by illegal wells serving farms "
                       "outside the official irrigation network.",
            "url": "https://www.nature.com/articles/s41598-023-39410-0",
        },
        {
            "year": 2020,
            "title": "Grand Ethiopian Renaissance Dam dispute intensifies",
            "summary": "As Ethiopia fills the GERD, Egypt faces reduced Nile flows. "
                       "Farmers increasingly turn to groundwater as a backup, accelerating "
                       "aquifer depletion in the delta.",
            "url": "https://www.bbc.com/news/world-africa-50328647",
        },
    ],
    "Punjab, India-Pakistan": [
        {
            "year": 2024,
            "title": "India's groundwater crisis: Punjab wells running dry",
            "summary": "Central Ground Water Board data shows 78% of Punjab's wells are "
                       "over-exploited. Rice paddy irrigation consumes 80% of extracted water. "
                       "Government pushes delayed planting to reduce pumping.",
            "url": "https://www.reuters.com/world/india/indias-breadbasket-running-out-water-2024-03-15/",
        },
        {
            "year": 2023,
            "title": "Free electricity fuels India's groundwater emergency",
            "summary": "Political parties compete to offer free farm electricity, removing "
                       "any cost signal for groundwater pumping. NASA GRACE satellites show "
                       "the Punjab aquifer losing 17.7 km\u00b3/year.",
            "url": "https://www.theguardian.com/global-development/2023/jul/17/india-groundwater-crisis",
        },
        {
            "year": 2009,
            "title": "NASA GRACE study reveals massive aquifer depletion",
            "summary": "Landmark study using NASA's GRACE satellite showed northwestern India "
                       "lost 109 km\u00b3 of groundwater between 2002-2008 — equivalent to "
                       "triple the capacity of Lake Mead.",
            "url": "https://www.nature.com/articles/nature08238",
        },
    ],
    "Central Valley, California": [
        {
            "year": 2024,
            "title": "SGMA deadline: California groundwater plans face scrutiny",
            "summary": "The 2024 deadline for Groundwater Sustainability Plans arrives. "
                       "Many basins in the San Joaquin Valley must now limit pumping or "
                       "fallow farmland. Farmers push back against water cuts.",
            "url": "https://calmatters.org/environment/2024/01/california-groundwater-sgma/",
        },
        {
            "year": 2023,
            "title": "Land subsidence accelerates in San Joaquin Valley",
            "summary": "Excessive groundwater pumping causes the ground to sink up to "
                       "1 foot per year in parts of the valley, damaging canals, roads, "
                       "and infrastructure worth billions.",
            "url": "https://www.usgs.gov/centers/ca-water-ls/land-subsidence-san-joaquin-valley",
        },
        {
            "year": 2014,
            "title": "California passes SGMA — first-ever statewide groundwater law",
            "summary": "The Sustainable Groundwater Management Act requires local agencies "
                       "to bring critically overdrafted basins to sustainability by 2040. "
                       "Historic first regulation of California groundwater.",
            "url": "https://water.ca.gov/Programs/Groundwater-Management/SGMA-Groundwater-Management",
        },
    ],
    "Aral Sea Basin, Central Asia": [
        {
            "year": 2023,
            "title": "Uzbekistan pledges to reduce cotton water use",
            "summary": "Facing international pressure, Uzbekistan commits to drip irrigation "
                       "for 1 million hectares of cotton by 2030. The Aral Sea remains at "
                       "10% of its 1960 volume.",
            "url": "https://www.theguardian.com/global-development/2023/aral-sea-uzbekistan-cotton",
        },
        {
            "year": 2018,
            "title": "Eastern Aral Sea basin dries up completely",
            "summary": "NASA satellite images show the eastern basin of the Aral Sea — once "
                       "the world's 4th largest lake — is completely dry for the second time "
                       "in modern history.",
            "url": "https://earthobservatory.nasa.gov/world-of-change/AralSea",
        },
    ],
    "Lake Naivasha, Kenya": [
        {
            "year": 2023,
            "title": "Lake Naivasha water levels drop as flower farms expand",
            "summary": "Cut flower exports to Europe have tripled since 2000, and Lake Naivasha "
                       "has dropped 3 meters. Environmental groups call for extraction caps, "
                       "but the industry employs 100,000+ workers.",
            "url": "https://www.theguardian.com/global-development/lake-naivasha-kenya-flowers",
        },
        {
            "year": 2010,
            "title": "WWF warns Lake Naivasha faces ecological collapse",
            "summary": "A WWF report documents how unregulated water extraction for horticulture "
                       "threatens the lake's hippo population, papyrus wetlands, and fishing communities.",
            "url": "https://www.wwf.org.uk/updates/lake-naivasha-dying",
        },
    ],
}

# --- Template for adding events ---
# Add to the relevant region's list:
#
# {
#     "year": 2025,
#     "title": "Short headline",
#     "summary": "2-3 sentence description of what happened and why it matters.",
#     "url": "https://...",
# },
