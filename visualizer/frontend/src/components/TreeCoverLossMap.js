import { LayersControl, MapContainer, TileLayer } from "react-leaflet";
import React, { useRef, useState } from "react";

import "leaflet/dist/leaflet.css"; // Leaflet styles
import "react-date-range/dist/styles.css"; // main style file
import "react-date-range/dist/theme/default.css"; // theme css file

import { DateRange } from "react-date-range";
import Legend from "./Legend";
import Level from "./Level";

const center = [-15.309707484568385, -59.65719598085998];
const zoom = 4;

// NOTE: Local api URL
const url = "http://127.0.0.1:8000/tiles/{z}/{x}/{y}.png";
// NOTE: Deployment api URL
// const url = 'https://maapvisualizer.herokuapp.com/tiles/{z}/{x}/{y}.png';

function TreeCoverLossMap() {
  const [startDate, setStartDate] = useState(new Date("Jan 1 2019"));
  const [endDate, setEndDate] = useState(new Date("Apr 29 2022"));

  const map = useRef(null);

  const handleSelect = (date) => {
    /**
     * Reformate the picked dates, and update the url used by the
     * leaflet to download the tiles.
     */
    setStartDate(date.selection.startDate);
    setEndDate(date.selection.endDate);
    const sy = date.selection.startDate.getFullYear();
    const sm = date.selection.startDate.getMonth() + 1;
    const sd = date.selection.startDate.getDate();
    const ey = date.selection.endDate.getFullYear();
    const em = date.selection.endDate.getMonth() + 1;
    const ed = date.selection.endDate.getDate();
    const start = `${sy}-${sm}-${sd}`;
    const end = `${ey}-${em}-${ed}`;
    map.current.setUrl(`${url}?start=${start}&end=${end}`);
  };

  const selectionRange = {
    startDate: startDate,
    endDate: endDate,
    key: "selection",
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      }}
    >
      <h1
        style={{
          padding: 10,
        }}
      >
        MAAP Visualizer
      </h1>
      <div
        style={{
          width: "100%",
          display: "grid",
          gridTemplateColumns: "25% 65%",
          gridAutoRows: "minmax(400px, 750px)",
          justifyContent: "space-evenly",
        }}
      >
        {/* Controll */}
        <div
          style={{
            overflowY: "auto",
          }}
        >
          <h2>Filters</h2>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              marginTop: 10,
            }}
          >
            <div
              style={{
                display: "flex",
                flexDirection: "column",
              }}
            >
              <h5>Year Range:</h5>
              <DateRange
                editableDateInputs={true}
                ranges={[selectionRange]}
                onChange={handleSelect}
              />
            </div>
          </div>
        </div>

        {/* Map */}
        <div id="map">
          <MapContainer
            style={{
              width: "100%",
              height: "100%",
            }}
            zoom={zoom}
            center={center}
            maxNativeZoom={18}
            maxZoom={22}
          >
            {/* render maptiler heybrid map */}
            <TileLayer
              attribution='<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'
              url="https://api.maptiler.com/maps/hybrid/256/{z}/{x}/{y}.jpg?key=XsGumaIy0N9p07zByHNB"
            />

            {/* render our processed tiles with a checkbox to show/hide the tiles layer */}
            <LayersControl>
              <LayersControl.Overlay
                checked
                name="Script generated tiles images"
              >
                <TileLayer url={url} ref={map} />
              </LayersControl.Overlay>
            </LayersControl>

            {/* Render the info divs legend and level */}
            <Legend />
            <Level val={zoom} />
          </MapContainer>
        </div>
      </div>
    </div>
  );
}

export default TreeCoverLossMap;
