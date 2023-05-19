import React from "react";
import Map from "react-map-gl";

const MapTest: React.FC = () => {
  return (
    <div
      className='col-span-12 rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark h-90 dark:bg-boxdark xl:col-span-7 xl:h-full'>
      <div className='w-full h-full'>
        <Map
          initialViewState={{
            longitude: 144.9631,
            latitude: -37.8136,
            zoom: 12,
          }}
          style={{width: '100%', height: '100%'}}
          mapStyle='mapbox://styles/mapbox/streets-v12'
          mapboxAccessToken={process.env.REACT_APP_MAPBOX_TOKEN}
        />
      </div>
    </div>
  )
}

export default MapTest;
