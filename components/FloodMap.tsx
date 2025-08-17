"use client";

import { useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, Circle, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// Fix for default markers in Next.js
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

interface FloodMapProps {
  center: [number, number];
  zoom: number;
  markers?: Array<{
    position: [number, number];
    title: string;
    riskLevel?: string;
  }>;
}

// Component to update map view
function ChangeView({ center, zoom }: { center: [number, number]; zoom: number }) {
  const map = useMap();
  useEffect(() => {
    map.setView(center, zoom);
  }, [center, zoom, map]);
  return null;
}

export default function FloodMap({ center, zoom, markers = [] }: FloodMapProps) {
  const getRiskColor = (riskLevel?: string) => {
    switch (riskLevel) {
      case "Very High":
        return "#FF0000";
      case "High":
        return "#FF6600";
      case "Medium":
        return "#FFCC00";
      case "Low":
        return "#00FF00";
      default:
        return "#0066FF";
    }
  };

  return (
    <MapContainer
      center={center}
      zoom={zoom}
      style={{ height: "320px", width: "100%" }}
      className="rounded-lg border border-slate-200"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <ChangeView center={center} zoom={zoom} />
      
      {markers.map((marker, index) => (
        <div key={index}>
          <Marker position={marker.position}>
            <Popup>
              <div className="text-center">
                <h3 className="font-semibold">{marker.title}</h3>
                {marker.riskLevel && (
                  <p className="text-sm mt-1">
                    Risk Level: <span className="font-medium">{marker.riskLevel}</span>
                  </p>
                )}
              </div>
            </Popup>
          </Marker>
          
          {marker.riskLevel && (
            <Circle
              center={marker.position}
              radius={1000}
              pathOptions={{
                color: getRiskColor(marker.riskLevel),
                fillColor: getRiskColor(marker.riskLevel),
                fillOpacity: 0.35,
                weight: 2,
              }}
            />
          )}
        </div>
      ))}
    </MapContainer>
  );
}