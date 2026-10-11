# Data sources and assumptions

## Real-data next milestone

IESO publishes demand reports and historical data through its [Data Directory](https://www.ieso.ca/en/power-data/data-directory) and [Hourly Demand Report directory](https://reports-public.ieso.ca/public/Demand/). Start with a small interval and inspect the actual report format before writing an adapter. No live downloader is implemented.

Do not confuse Ontario demand with market demand. Verify whether source hours identify the beginning or end of intervals and whether they use Eastern Standard Time or a daylight-saving-aware timezone. The importer accepts **whole-hour timestamps with an explicit UTC offset** and converts them to UTC. It does not infer an IESO time convention.

Input CSV columns: `timestamp,demand_mw,temperature_c`. Example timestamp: `2025-01-01T00:00:00+00:00`. Demand is MW and temperature is degrees Celsius. Temperature must already be aligned to the same hour; missing values are rejected rather than silently imputed.

For real data: `python run.py --input data/raw/observations.csv --source "YOUR_DATASET_URL_OR_ID"`. Add a manifest documenting demand and weather sources, retrieval date, coverage, units, conversions, and usage terms. Source references were checked on 2026-10-10. No third-party dataset is bundled.
