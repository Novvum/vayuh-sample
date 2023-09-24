import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const TemperatureMap = () => {
  const [geojsonData, setGeojsonData] = useState(null);

  useEffect(() => {
    // Fetch the GeoJSON data
    fetch('output.geojson')
      .then((response) => response.json())
      .then((data) => setGeojsonData(data))
      .catch((error) => console.error('Error fetching GeoJSON file:', error));
  }, []);

  const getColor = (temperature) => {
    // Replace with your color scale
    return temperature > 30 ? '#800026' :
           temperature > 25 ? '#BD0026' :
           temperature > 20 ? '#E31A1C' :
           temperature > 15 ? '#FC4E2A' :
           temperature > 10 ? '#FD8D3C' :
                              '#FFEDA0';
  };

  const geoJSONStyle = (feature) => {
    return {
      fillColor: getColor(feature.properties.temperature),
      weight: 2,
      opacity: 1,
      color: 'white',
      dashArray: '3',
      fillOpacity: 0.7,
    };
  };

  return (
    <MapContainer center={[37.8, -96]} zoom={4} style={{ width: '100%', height: '100vh' }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {geojsonData && <GeoJSON data={geojsonData} style={geoJSONStyle} />}
    </MapContainer>
  );
};

export default TemperatureMap;
