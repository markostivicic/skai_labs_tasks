(function () {
    // Fetching polygon data from JSON file
    fetch("polygon.json")
        .then((response) => response.json())
        .then((data) => {
            // Initializing the map
            const map = new ol.Map({
                target: "map", // Setting the target to the map (ID of the element)
                layers: [
                    new ol.layer.Tile({ // Adding a tile layer (OSM) as the base layer
                        source: new ol.source.OSM(),
                    }),
                ],
                view: new ol.View({ // Setting the initial view of the map
                    center: ol.proj.fromLonLat([37.41, 8.82]), // Setting the center of the map (geographical coordinates)
                    zoom: 4, // Setting the zoom level
                }),
            });

            // Checking the validity of the polygon data
            if (Array.isArray(data.polygon) && data.polygon.length >= 6) {
                const coordinates = data.polygon; // Retrieving the polygon coordinates
                // Checking the validity of each coordinate
                if (coordinates.every(coordinate => Array.isArray(coordinate) && coordinate.length === 2)) {
                    // Creating a feature (polygon) using OpenLayers geometry
                    const polygon = new ol.Feature({
                        geometry: new ol.geom.Polygon(coordinates)
                    });

                    // Creating a vector data source
                    const vectorSource = new ol.source.Vector({
                        features: [polygon],
                    });

                    // Creating a vector data layer and adding it to the map
                    const vectorLayer = new ol.layer.Vector({
                        source: vectorSource,
                    });
                    map.addLayer(vectorLayer);

                    // Fitting the map view so that the entire polygon is visible
                    const geometry = polygon.getGeometry();
                    if (geometry && geometry.getType() === "polygon")
                        map.getView().fit(geometry.getExtent(), map.getSize());
                } else {
                    console.error("Invalid polygon data:", data.polygon); // Logging a message about invalid polygon data
                }
            } else {
                console.error("Invalid polygon data:", data.polygon); // Logging a message about invalid polygon data
            }
        })
        .catch((error) => console.log(error)); // Handling and logging errors
})();
