import React, {useEffect} from "react";
import {MapProvider, Map, useMap} from "react-map-gl";
import SaLayer from "./SaLayer";


const MapHomeless: React.FC = () => {
  return (
    <MapProvider>
      <div
        className='col-span-12 rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark h-90 dark:bg-boxdark xl:col-span-8 xl:h-full'>
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
            <SaLayer/>
          </Map>
        </div>
      </div>
    </MapProvider>
  )
}

export default MapHomeless;
