import { useEffect } from "react";
import L from "leaflet";
import { useMap } from "react-leaflet";

function Legend() {
  const map = useMap();
  useEffect(() => {
    var legend = document.getElementsByClassName("legend");
    if (legend.length) return;
    if (map) {
      const legend = L.control({ position: "bottomright" });

      legend.onAdd = () => {
        const div = L.DomUtil.create("div", "info legend");
        div.innerHTML = `
        <div class='legend-element'>
          <div class='legend-color' style='background-color:rgb(19,69,139)'></div>
          <div class='legend-description'>Low confidence</div>
        </div>
        <div class='legend-element'>
          <div class='legend-color' style='background-color:rgb(222,196,176)'></div>
          <div class='legend-description'>Medium confidence</div>
        </div>
        <div class='legend-element'>
          <div class='legend-color' style='background-color:rgb(255, 0, 0)'></div>
          <div class='legend-description'>High confidence</div>
        </div>
        `;
        return div;
      };

      legend.addTo(map);
    }
  }, [map]);
  return null;
}

export default Legend;
