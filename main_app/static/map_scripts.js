mapboxgl.accessToken = 'pk.eyJ1Ijoic2dyaWZmaXRoczEyIiwiYSI6ImNsNDMzdGo4ZDB4em4za282cmJhemFka24ifQ.m4ufhKsweS1MWLuCvNigvA';
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/light-v10',
  center: [-96, 37.8],
  zoom: 0
});
const geojson = {
  type: 'FeatureCollection',
  features: [
   {{ posts | safe }}
  ]
};
// add markers to map
for (const feature of geojson.features) {
  // create a HTML element for each feature
  const el = document.createElement('div');
  el.className = 'marker';
  // make a marker for each feature and add to the map
  new mapboxgl.Marker(el)
  .setLngLat(feature.geometry.coordinates)
  .setPopup(
    new mapboxgl.Popup({ offset: 25 }) // add popups
      .setHTML(
        `<h3>${feature.properties.title}</h3>
        <h1>${feature.properties.link}</h1>
        <img src="${feature.properties.image}" width = "100" height = "100">`
      )
  )
  .addTo(map);
}