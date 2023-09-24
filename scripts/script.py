import numpy as np
import geopandas as gpd
from shapely.geometry import Point, box
import h5py

# Define the path to the h5 file and US boundary file
file_path = 'sample_data.h5'
us_boundary_path = 'usa.geojson'  # Replace with the actual path to your US boundary file

# Read the US boundary
us_boundary_gdf = gpd.read_file(us_boundary_path)
us_boundary = us_boundary_gdf.geometry.unary_union

# Read the h5 file
with h5py.File(file_path, 'r') as file:
    group = file['df']
    data = group['block0_values'][:]
    col_names = [name.decode('utf-8') for name in group['block0_items'][:]]

# Print the first few lat, lon, and temperature from the sample file
print("First few lat, lon, and temperature values from the sample file:")
for i, (lat, lon, temp) in enumerate(data):
    if i == 5:  # Adjust the number to print more or fewer rows
        break
    print(f"{i+1}. Latitude: {lat}, Longitude: {lon}, Temperature: {temp}")

# Create a GeoDataFrame from the data
data_dicts = [{'latitude': lat, 'longitude': (lon + 180) % 360 - 180, 'temperature': temp} for lat, lon, temp in data]
gdf = gpd.GeoDataFrame(data_dicts)
gdf['geometry'] = gdf.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)

# Make sure that gdf has a CRS
gdf.crs = 'EPSG:4326'  # WGS 84

# Ensure the GeoDataFrames have the same CRS before spatial operations
if gdf.crs != us_boundary_gdf.crs:
    gdf = gdf.to_crs(us_boundary_gdf.crs)

# print(gdf.head())

# Define the square size and create bounding box (square) polygons
square_size = 0.5
minx, miny, maxx, maxy = us_boundary.bounds
x_coords = np.arange(minx, maxx, square_size)
y_coords = np.arange(miny, maxy, square_size)

# Create a GeoDataFrame with rectangles
rects = []
for x in x_coords:
    for y in y_coords:
        rects.append(box(x, y, x + square_size, y + square_size))
rect_gdf = gpd.GeoDataFrame(geometry=rects)
rect_gdf['temperature'] = np.nan


rect_gdf.crs = 'EPSG:4326'
# print(rect_gdf.head())

# Assign temperature to each rectangle
def assign_temperature(rect):
    # print(f"Processing rectangle with bounds: {rect['geometry'].bounds}")
    # print(rect['geometry'])
    within_points = gdf[gdf.within(rect['geometry'])]
    if not within_points.empty:
        print(f"Found {len(within_points)} points from sample_data.h5 within the rectangle.")
        print("Points:")
        print(within_points)
        mean_temperature = within_points['temperature'].mean()
        print(f"Assigning mean temperature: {mean_temperature} to the rectangle.")
        rect['temperature'] = mean_temperature
    # else:
    #     print("No points from sample_data.h5 found within the rectangle. Leaving temperature as NaN.")
    return rect

rect_gdf = rect_gdf.apply(assign_temperature, axis=1)

# Clip rectangles to US boundary
clipped_rect_gdf = gpd.clip(rect_gdf, us_boundary_gdf)
clipped_rect_gdf.to_file('./vayuh-webapp/public/output.geojson', driver='GeoJSON')

print("GeoJSON file has been written to 'output.geojson'")
