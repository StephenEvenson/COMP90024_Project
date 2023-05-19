import React from "react";
import Map from "react-map-gl";

const MapTest: React.FC = () => {
  return (
    <div className='h-full'>
      <div className='w-full h-full'>
        <Map
          initialViewState={{
            longitude: 144.9631,
            latitude: -37.8136,
            zoom: 12,
          }}
          style={{width: '100%', height: '100%'}}
          mapStyle='mapbox://styles/mapbox/streets-v11'
          mapboxAccessToken={process.env.REACT_APP_MAPBOX_TOKEN}
        />
      </div>
    </div>
  )
}

export default MapTest;
