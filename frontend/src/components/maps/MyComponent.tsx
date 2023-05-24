import {useMap} from "react-map-gl";
import {useEffect, useRef} from "react";
import mapboxgl from "mapbox-gl";
import ReactDOM from "react-dom/client"

const Popup = (props:{
  title?: string,
  description?: string,
}) => (
  <div className='p-2 max-w-40 overflow-clip'>
    <div className='text-lg font-bold'>{props.title || 'Title'}</div>
    <div className='text-sm'>{props.description || 'Description'}</div>
  </div>
)


export default function () {
  const {myMap: mapRef} = useMap()
  const popUpRef = useRef(new mapboxgl.Popup({offset: 15}))

  function loadMap() {
    console.log('loadMap')
    const map: mapboxgl.Map = mapRef!.getMap()
    map.addControl(new mapboxgl.FullscreenControl())
    map.addControl(new mapboxgl.GeolocateControl())
    map.addControl(new mapboxgl.NavigationControl())
    map.addControl(new mapboxgl.ScaleControl(
      {maxWidth: 80, unit: 'metric'},
    ), 'top-right')

    map.addSource('phns', {
      'type': 'geojson',
      'data': '/GeoJson/phn.geojson',
      'generateId': true // This ensures that all features have unique IDs
    });

    // The feature-phn dependent fill-opacity expression will render the hover effect
    // when a feature's hover phn is set to true.
    map.addLayer({
      'id': 'phn-fills',
      'type': 'fill',
      'source': 'phns',
      'layout': {},
      'paint': {
        // 'fill-color': '#627BC1',
        'fill-color': [
          'interpolate',
          ['linear'],
          ['get', 'SUM_AREASQ'],
          0,
          '#F2F12D',
          100,
          '#EED322',
          1000,
          '#E6B71E',
          5000,
          '#DA9C20',
          10000,
          '#CA8323',
          50000,
          '#B86B25',
          100000,
          '#A25626',
          500000,
          '#8B4225',
          1000000,
          '#723122'
        ],
        'fill-opacity': [
          'case',
          ['boolean', ['feature-state', 'hover'], false],
          1,
          0.5
        ]
      }
    });

    map.addLayer({
      'id': 'phn-borders',
      'type': 'line',
      'source': 'phns',
      'layout': {},
      'paint': {
        'line-color': '#627BC1',
        'line-width': 1
      }
    });
    let hoveredPhnId: number | null = null;
    // When the user moves their mouse over the phn-fill layer, we'll update the
    // feature phn for the feature under the mouse.
    map.on('mousemove', 'phn-fills', (e) => {
      if (e.features!.length > 0) {
        if (hoveredPhnId !== null) {
          map.setFeatureState(
            {source: 'phns', id: hoveredPhnId},
            {hover: false}
          );
        }
        // console.log(e.features![0])
        hoveredPhnId = e.features![0].id as number;
        map.setFeatureState(
          {source: 'phns', id: hoveredPhnId},
          {hover: true}
        );
      }
    });

    // When the mouse leaves the phn-fill layer, update the feature phn of the
    // previously hovered feature.
    map.on('mouseleave', 'phn-fills', () => {
      if (hoveredPhnId !== null) {
        map.setFeatureState(
          {source: 'phns', id: hoveredPhnId},
          {hover: false}
        );
      }
      hoveredPhnId = null;
    });


    /**
     * Start popup
     **/
    map.on('click', 'phn-fills', (e) => {
      const popupNode = document.createElement("div")
      const pop = ReactDOM.createRoot(popupNode)
      pop.render(<Popup title={'click'} description={e.lngLat.toString()}/>)
      popUpRef.current
        .setLngLat(e.lngLat)
        .setDOMContent(popupNode)
        .addTo(map)
    });
    /**
     *  End popup
     */

    // console.log(map)
    console.log('finish loadMap')
  }

  useEffect(() => {
    // console.log(mapRef)
    if (mapRef) {
      mapRef.on('load', loadMap)
    }
  }, [mapRef])
  return (
    <></>
  )
}