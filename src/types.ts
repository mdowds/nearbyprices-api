export interface PricesForOutcode {
    readonly areaName: string,
    readonly averagePrice: number,
    readonly detachedAverage?: number,
    readonly flatAverage?: number,
    readonly outcode: string,
    readonly semiDetachedAverage?: number,
    readonly terracedAverage?: number,
    readonly transactionCount: number
}

export interface Position {
    lat: number,
    long: number
}

interface AddressComponent {
    long_name: string,
    short_name: string,
    types: string
}

export interface ReverseGeocodingResults {
    results: [
        {
            address_components: AddressComponent[]
        }
    ]
    status : string
}