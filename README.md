#Few assumptions/things to keep in mind - 

1. As I see on the (https://vayuh-web-app.web.app/) there are grids on the US map which match to a temperature value (using a color scale); but the granularity of the data you send us was much smaller, so the values are scattered on the map. If I increase the  rectangle grid size and then that gives a much better picture. Or alternatively we can calculate the temperature with the nearest neighbour. So that is based on the use case we are targeting. So I have't done all those for now, but can be easily achieved. 
2. Since it was Lat/longitude values, I have taken the mean of the temperature value which falls on that particular grid in the map.
3. The US map coordinates I am using does take in some water bodies as well, so the map is a little spilling in those areas. Can be resolved easily with a better US geoJSON file.
4. I am using Leaflet.js for rendering the map, but we can definitely use MapboxGL (as you are doing in your webapp)
5. I am currently converting the hdf5 files into geoJSON files because that serves best for the web. I am using a python script (h5py, Geopandas) for reading h5 file, creating grid polygons and clipping on the US map.
6. I just put together this in a couple of hours, so I haven't run it through code quality, performance or browser compatibility. 