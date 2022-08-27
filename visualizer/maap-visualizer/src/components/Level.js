import { useEffect } from "react";
import L from "leaflet";
import { useMap, useMapEvents } from "react-leaflet";

function Level({ val }) {
  const map = useMap();
  const mapEvents = useMapEvents({
    zoomend: () => {
      const level = document.getElementsByClassName("level");
      if (!level.length) return;
      level[0].innerHTML = `Level: ${mapEvents.getZoom()}`
    },
  });

  useEffect(() => {
    var level = document.getElementsByClassName("level");
    if (level.length) return;
    if (map) {
      const level = L.control({ position: "bottomleft" });
      level.onAdd = () => {
        const div = L.DomUtil.create("div", "info level");
        div.innerHTML = `Level: ${val}`;
        return div;
      };

      level.addTo(map);
    }

  }, [map, val]);
  return null;
}

export default Level;
