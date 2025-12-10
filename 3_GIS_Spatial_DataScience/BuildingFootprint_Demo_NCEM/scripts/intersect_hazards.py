import geopandas as gpd
import pandas as pd
import os

BUILDINGS_PATH = "data_clean/buildings_cleaned.gpkg"
FLOOD_PATH = "hazards/flood_fema_nfhl.gpkg"
OUT_GPKG = "hazards/buildings_in_floodzones.gpkg"
SUMMARY_CSV = "hazards/flood_exposure_summary.csv"

def main():
    print("[*] Loading cleaned building footprints...")
    buildings = gpd.read_file(BUILDINGS_PATH)

    print("[*] Loading FEMA flood hazard layer...")
    flood = gpd.read_file(FLOOD_PATH)

    # FEMA zones to include
    valid_zones = ["A", "AE", "AO", "AH", "VE", "V"]
    if "FLD_ZONE" in flood.columns:
        flood = flood[flood["FLD_ZONE"].isin(valid_zones)]
        print(f"[INFO] Using FEMA zones: {valid_zones}")

    print("[*] Reprojecting both layers to a metric CRS (EPSG:3857)...")
    buildings = buildings.to_crs(3857)
    flood = flood.to_crs(3857)

    print("[*] Performing spatial intersection...")
    flooded = gpd.overlay(buildings, flood, how="intersection")

    print("[*] Saving intersected buildings...")
    os.makedirs("hazards", exist_ok=True)
    flooded.to_file(OUT_GPKG, driver="GPKG")

    print("[*] Generating summary statistics...")
    total_buildings = len(buildings)
    flooded_buildings = len(flooded)

    pct_exposed = round((flooded_buildings / total_buildings) * 100, 2)

    summary = pd.DataFrame({
        "total_buildings": [total_buildings],
        "flood_exposed": [flooded_buildings],
        "percent_exposed": [pct_exposed]
    })

    summary.to_csv(SUMMARY_CSV, index=False)

    print("[SUCCESS] Analysis complete.")
    print(f" - Flooded buildings: {flooded_buildings}")
    print(f" - Percent exposed: {pct_exposed}%")
    print(f" - Output saved to: {OUT_GPKG}")
    print(f" - Summary saved to: {SUMMARY_CSV}")

if __name__ == "__main__":
    main()
