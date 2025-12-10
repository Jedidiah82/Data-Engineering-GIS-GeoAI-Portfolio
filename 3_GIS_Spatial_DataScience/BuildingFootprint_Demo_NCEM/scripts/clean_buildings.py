import geopandas as gpd
import os

RAW_PATH = "data_raw/microsoft_footprints.geojson"
OUTPUT_PATH = "data_clean/buildings_cleaned.gpkg"
QAQC_REPORT = "data_clean/buildings_qaqc_report.md"


def main():
    # Check input exists
    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError(f"Missing input file: {RAW_PATH}")

    print("[*] Loading raw building footprints...")
    buildings = gpd.read_file(RAW_PATH)

    print("[*] Calculating polygon areas...")
    buildings["area_m2"] = buildings.geometry.area

    print("[*] Removing tiny polygons (< 30 m²)...")
    before_count = len(buildings)
    buildings = buildings[buildings["area_m2"] > 30]
    after_count = len(buildings)

    print(f"[INFO] Removed {before_count - after_count} tiny polygons.")

    print("[*] Fixing invalid geometries...")
    buildings["geometry"] = buildings["geometry"].buffer(0)

    print("[*] Adding perimeter field...")
    buildings["perimeter_m"] = buildings.geometry.length

    # Save cleaned dataset
    print(f"[*] Saving cleaned dataset to: {OUTPUT_PATH}")
    buildings.to_file(OUTPUT_PATH, driver="GPKG")

    # Generate basic QA/QC report
    print(f"[*] Writing QA/QC report to: {QAQC_REPORT}")
    with open(QAQC_REPORT, "w") as report:
        report.write("# QA/QC Report — Cleaned Building Footprints\n\n")
        report.write(f"- Raw polygons: {before_count}\n")
        report.write(f"- After cleaning: {after_count}\n")
        report.write(f"- Removed tiny polygons: {before_count - after_count}\n")
        report.write("- Invalid geometries corrected using buffer(0)\n")

    print("[SUCCESS] Cleaning complete. Process finished successfully.")


if __name__ == "__main__":
    main()
