import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
from shapely.geometry import box
import contextily as ctx

def add_north_arrow(ax, size=0.1):
    ax.annotate('N', xy=(0.95, 0.2), xytext=(0.95, 0.3),
                arrowprops=dict(facecolor='black', width=5, headwidth=15),
                ha='center', va='center', fontsize=14,
                xycoords=ax.transAxes)

def create_inset(ax, aoi_bounds):
    inset = ax.inset_axes([0.02, 0.65, 0.22, 0.3])
    nc = gpd.read_file("https://raw.githubusercontent.com/johan/world.geo.json/master/countries/USA/NC.geo.json")

    nc.plot(ax=inset, color="#efefef", edgecolor="black")
    
    minx, miny, maxx, maxy = aoi_bounds
    inset.plot(gpd.GeoSeries(box(minx, miny, maxx, maxy)), 
               ax=inset, color="red", alpha=0.5)
    
    inset.set_xticks([])
    inset.set_yticks([])
    inset.set_title("NC Inset Map", fontsize=8)

def main():
    buildings = gpd.read_file("hazards/buildings_in_floodzones.gpkg")
    flood = gpd.read_file("hazards/flood_fema_nfhl.gpkg")

    # Reproject to Web Mercator for basemap
    buildings = buildings.to_crs(3857)
    flood = flood.to_crs(3857)

    fig, ax = plt.subplots(figsize=(12, 12))

    # Plot FEMA flood zones
    flood.plot(ax=ax, color="#77aaff", alpha=0.4, edgecolor="blue", linewidth=0.5, label="Flood Hazard")

    # Plot exposed buildings
    buildings.plot(ax=ax, color="red", markersize=1, label="Exposed Buildings")

    # Basemap
    ctx.add_basemap(ax, source=ctx.providers.Stamen.TonerLite)

    # Add NCEM map elements
    add_north_arrow(ax)
    create_inset(ax, buildings.total_bounds)

    # Scalebar
    scalebar = ScaleBar(dx=1, units="m", location="lower left")
    ax.add_artist(scalebar)

    ax.set_title("NCEM-Style Flood Exposure Map\nFEMA Flood Zones + Building Footprints", fontsize=16)
    ax.legend()

    ax.set_axis_off()

    fig.savefig("figures/flood_exposure_map_ncem.png", dpi=300)
    print("[SUCCESS] NCEM-style map saved at figures/flood_exposure_map_ncem.png")

if __name__ == "__main__":
    main()
