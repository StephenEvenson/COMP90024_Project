import {Layer, Source, useMap} from "react-map-gl";
import {useEffect, useRef, useState} from "react";
import mapboxgl from "mapbox-gl";
import ReactDOM from "react-dom/client"
import useData from "../../hooks/useData";
import {Sa4SudoHomeless} from "../../types";
// @ts-ignore
import s4geojson from "./2011sa4.geojson";

const Popup = (props: {
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
  const [geojsonData, setGeojsonData] = useState<any>(null)
  const [fianlGeojsonData, setFinalGeojsonData] = useState<any>(null)


  useEffect(() => {
    fetch('/geojsons/2011sa4.geojson')
      .then(response => response.json())
      .then(data => {
        setGeojsonData(data);
      })
      .catch(error => console.error('Error:', error));
  }, [])

  const [{data}] = useData('/sudo/sudo_sa4_homeless', undefined) as any
  const homelessData = data?.docs as Sa4SudoHomeless[]
  if (homelessData && s4geojson.features) {
    homelessData?.forEach((homeless, index) => {
      s4geojson.features[index].properties.homeless = homeless
    })
  }

  useEffect(() => {
    fetch('/geojsons/2011sa4.geojson')
      .then(response => response.json())
      .then(data => {
        setGeojsonData(data);
      })
      .catch(error => console.error('Error:', error));
  }, [])

  useEffect(() => {
    if (geojsonData && homelessData) {
      // console.log(geojsonData, homelessData)
      const homelessDictionary = homelessData.reduce((acc, item) => {
        const key = item.sa4_code16;
        const value = {
          // @ts-ignore
          sa4_name_2016: item.sa4_name_2016,
          homeless_total: item.homeless_total
        };
        // @ts-ignore
        acc[key] = value;
        return acc;
      }, {});
      const new_json = JSON.parse(JSON.stringify(geojsonData))
      new_json.features.forEach((feature: any, index: any) => {
        // console.log(feature.properties)
        const SA4_CODE = feature.properties.SA4_CODE
        // @ts-ignore
        const homeless = homelessDictionary[parseInt(SA4_CODE)]
        if (homeless) {
          feature.properties.homeless = homeless.homeless_total as number
        }
      })
      setFinalGeojsonData(new_json)
    }
  }, [geojsonData, homelessData])

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
      pop.render(<Popup title={'click'} description={e.lngLat.toString()}/>)
      popUpRef.current
        .setLngLat(e.lngLat)
        .setDOMContent(popupNode)
        .addTo(map)
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
        ['get', 'homeless'],
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
    <Source id={'sa4'} type='geojson' data={fianlGeojsonData} generateId={true}>
      {/*@ts-ignore */}
      <Layer {...borderLayer} />
      {/*@ts-ignore */}
      <Layer {...fillLayer} />
      {/*@ts-ignore */}
      {/*<Layer {...HeatmapLayer}/>*/}
    </Source>

  )
}