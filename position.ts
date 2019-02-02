import fetch from 'node-fetch';
import {Position, ReverseGeocodingResults} from "./src/types";
import Firestore = FirebaseFirestore.Firestore;
import pricesForOutcode from "./src/outcode";

export default async function pricesForPosition(db: Firestore, position: Position) {
    const url = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${position.lat},${position.long}&key=${process.env.GMAPS_API_KEY}`;
    const results: ReverseGeocodingResults = await fetch(url).then(r => r.json());

    const postcode = results.results[0].address_components.find(ac => ac.types.includes('postal_code'));
    const outcode = postcode.long_name.split(' ')[0];

    return await pricesForOutcode(db, outcode);
}