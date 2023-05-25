import {Layer, Source, useMap} from "react-map-gl";
import {useEffect, useRef, useState} from "react";
import mapboxgl from "mapbox-gl";
import ReactDOM from "react-dom/client"

import {getSa4CombineHomelessHeat} from "../../api/api";

const Popup = (props: {
  properties: any,
  title?: string,
}) => {
  // console.log(props.e.features.properties)
  const {properties} = props
  return (
    <div className='p-2 max-w-80 overflow-clip'>
      <div className='text-base font-bold text-black-2'>{properties.SA4_NAME || 'Title'}</div>
      <div className='flex space-x-2'>
        <div>Homeless number:</div>
        <div className=''> {properties.homeless_total}</div>
      </div>
      <div className='flex space-x-2'>
        <div>Homeless heat:</div>
        <div className=''> {properties.homeless_heat ? properties.homeless_heat .toFixed(2) : 0}</div>
      </div>
    </div>
  )
}


export default function () {
  const {myMap: mapRef} = useMap()
  const popUpRef = useRef(new mapboxgl.Popup({offset: 15}))
  const [geojsonData, setGeojsonData] = useState<any>(null)

  useEffect(() => {
    getSa4CombineHomelessHeat().then((data) => {
      setGeojsonData(data);
      console.log(data)
      // console.log({'geojsonData': data})
    })
  }, [])

  function loadMap() {
    console.log('loadMap')
    const map: mapboxgl.Map = mapRef!.getMap()
    map.addControl(new mapboxgl.FullscreenControl())
    map.addControl(new mapboxgl.GeolocateControl())
    map.addControl(new mapboxgl.NavigationControl())
    map.addControl(new mapboxgl.ScaleControl(
      {maxWidth: 80, unit: 'metric'},
    ), 'top-right')


    let hoveredAreaId: number | null = null;
    // When the user moves their mouse over the phn-fill layer, we'll update the
    // feature phn for the feature under the mouse.
    map.on('mousemove', 'sa4-fills', (e) => {
      if (e.features!.length > 0) {
        if (hoveredAreaId !== null) {
          map.setFeatureState(
            {source: 'sa4', id: hoveredAreaId},
            {hover: false}
          );
        }
        // console.log(e.features![0])
        hoveredAreaId = e.features![0].id as number;
        map.setFeatureState(
          {source: 'sa4', id: hoveredAreaId},
          {hover: true}
        );
      }
    });

    // When the mouse leaves the phn-fill layer, update the feature phn of the
    // previously hovered feature.
    map.on('mouseleave', 'sa4-fills', () => {
      if (hoveredAreaId !== null) {
        map.setFeatureState(
          {source: 'sa4', id: hoveredAreaId},
          {hover: false}
        );
      }
      hoveredAreaId = null;
    });

    map.on('click', 'sa4-fills', (e) => {
      const popupNode = document.createElement("div")
      const pop = ReactDOM.createRoot(popupNode)
      const features = map.queryRenderedFeatures(e.point, {layers: ['sa4-fills']});
      if (features.length > 0) {
        const properties = features[0].properties;
        // console.log(properties);
        pop.render(<Popup properties={properties}/>)
        popUpRef.current
          .setLngLat(e.lngLat)
          .setDOMContent(popupNode)
          .addTo(map)
      }
    });
    // console.log(map)
    console.log('finish loadMap')
  }

  useEffect(() => {
    // console.log(mapRef)
    if (mapRef) {
      mapRef.on('load', loadMap)
    }
  }, [mapRef])

  const borderLayer = {
    'id': 'sa4-borders',
    'type': 'line',
    'source': 'sa4',
    'layout': {},
    'paint': {
      'line-color': '#627BC1',
      'line-width': 1
    }
  }

  const fillLayer = {
    'id': 'sa4-fills',
    'type': 'fill',
    'source': 'sa4',
    'layout': {},
    'paint': {
      // 'fill-color': '#627BC1',
      'fill-color': [
        'interpolate',
        ['linear'],
        ['get', 'homeless_total'],
        0,
        '#F2F12D',
        100,
        '#EED322',
        1000,
        '#E6B71E',
        2000,
        '#DA9C20',
        4000,
        '#CA8323',
        5000,
        '#B86B25',
        10000,
        '#A25626',
        20000,
        '#8B4225',
        // 100,
        // '#723122'
      ],
      'fill-opacity': [
        'case',
        ['boolean', ['feature-state', 'hover'], false],
        1,
        0.5
      ]
    }
  }

  return (
    // @ts-ignore
    <Source id={'sa4'} type='geojson' data={geojsonData} generateId={true}>
      {/*@ts-ignore */}
      <Layer {...borderLayer} />
      {/*@ts-ignore */}
      <Layer {...fillLayer} />
      {/*@ts-ignore */}
      {/*<Layer {...HeatmapLayer}/>*/}
    </Source>

  )
}