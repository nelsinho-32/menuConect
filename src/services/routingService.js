// src/services/routingService.js

export async function getRoute(startCoords, endCoords) {
  //
  // -----------------------------------------------------------------
  // COLE A SUA CHAVE DE API DO OPENROUTESERVICE AQUI
  // -----------------------------------------------------------------
  //
  const apiKey = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImZlYzUyYmZlMzdlOTRiZjNiOTY3YzM3YjU3NGZkMzllIiwiaCI6Im11cm11cjY0In0=";
  //
  // -----------------------------------------------------------------
  //

  if (!apiKey || apiKey === "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImZlYzUyYmZlMzdlOTRiZjNiOTY3YzM3YjU3NGZkMzllIiwiaCI6Im11cm11cjY0In0=") {
    console.error("A chave da API do OpenRouteService não foi definida.");
    // Lança um erro para que o componente o possa apanhar
    throw new Error("A chave da API de Rotas não está configurada.");
  }

  const apiUrl = 'https://api.openrouteservice.org/v2/directions/driving-car/geojson';

  const body = {
    "coordinates": [
      [startCoords.longitude, startCoords.latitude],
      [endCoords.longitude, endCoords.latitude]
    ]
  };

  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      body: JSON.stringify(body),
      headers: {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Content-Type': 'application/json',
        'Authorization': apiKey
      }
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`Erro da API de Rotas: ${errorData.error.message}`);
    }

    const data = await response.json();
    
    // A API devolve as coordenadas em [longitude, latitude], precisamos de as inverter para o Leaflet
    const routeCoordinates = data.features[0].geometry.coordinates.map(coord => [coord[1], coord[0]]);
    
    return routeCoordinates;

  } catch (error) {
    console.error('Falha ao obter a rota:', error);
    throw error; // Re-lança o erro para o componente
  }
}