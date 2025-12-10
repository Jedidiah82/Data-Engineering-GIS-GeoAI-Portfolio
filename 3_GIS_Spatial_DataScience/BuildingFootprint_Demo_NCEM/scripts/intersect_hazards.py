import geopandas as gpd
import os

CLEANED_BUILDINGS = "data_clean/buildings_cleaned.gpkg"
HAZARD_FILE = "hazards/flood_fema_nfhl.gpkg"   # You can swap this out
OUTPUT_PATH = "data_clean/buildings_exposure.gpkg"


def main():
    # Check inputs
    if not os.path.exists(CLEANED_BUILDINGS):
        raise FileNotFoundError(f"Missing cleaned footprints: {CLEANED_BUILDINGS}")

    if not os.path.exists(HAZARD_FILE):
        raise FileNotFoundError(f"Missing hazard dataset: {HAZARD_FILE}")

    print("[*] Loading cleaned buildings...")
    buildings = gpd.read_file(CLEANED_BUILDINGS)

    print("[*] Loading hazard layer...")
    hazard = gpd.read_file(HAZARD_FILE)

    print("[INFO] Reprojecting hazard layer to match buildings CRS...")
    hazard = hazard.to_crs(buildings.crs)

    print("[*] Performing spatial intersection...")
    exposure = gpd.overlay(buildings, hazard, how="intersection")

    print("[*] Saving results to:", OUTPUT_PATH)
    exposure.to_file(OUTPUT_PATH, driver="GPKG")

    # Summary
    print("\n[SUCCESS] Hazard exposure intersection complete.")
    print(f"- Buildings with exposure: {len(exposure)}")
    print(f"- Output saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
