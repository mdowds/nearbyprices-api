const MAXIMUM_LATITUDE = 60.86;
const MINIMUM_LATITUDE = 49.86;
const MAXIMUM_LONGITUDE = 1.78;
const MINIMUM_LONGITUDE = -8.45;

export function validateLatitude(lat) {
    console.log(lat, lat > MAXIMUM_LATITUDE, lat < MINIMUM_LATITUDE);
    if (lat > MAXIMUM_LATITUDE || lat < MINIMUM_LATITUDE || isNaN(lat)) {
        throw new Error('Latitude is not valid. It must be within the UK.')
    } else {
        return true;
    }
}

export function validateLongitude(long) {
    if (long > MAXIMUM_LONGITUDE || long < MINIMUM_LONGITUDE || isNaN(long)) {
        throw new Error('Longitude is not valid. It must be within the UK.')
    } else {
        return true;
    }
}