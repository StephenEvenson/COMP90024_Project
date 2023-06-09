import React from "react";
import {MapProvider, Map} from "react-map-gl";
import SaHomeLessLayer from "./SaHomelessLayer";


const MapHomeless: React.FC = () => {
  return (
    <MapProvider>
      <div
        className='col-span-12 rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark h-90 dark:bg-boxdark xl:col-span-12 xl:h-150'>
        <div className='w-full h-full'>
          <Map
            id='myMap'
            initialViewState={{
              longitude: 130.9631,
              latitude: -24.5136,
              zoom: 2.4,
            }}
            style={{width: '100%', height: '100%'}}
            mapStyle='mapbox://styles/mapbox/streets-v12'
            mapboxAccessToken={process.env.REACT_APP_MAPBOX_TOKEN}
          >
            <SaHomeLessLayer/>
          </Map>
        </div>
      </div>
    </MapProvider>
  )
}

export default MapHomeless;
