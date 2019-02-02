const fetch = require('node-fetch');

let pricesForPosition;

describe('GET /prices/position', () => {
    beforeAll(async () => {
        pricesForPosition = await fetch('http://localhost:5100/prices/position?lat=51.747124&long=-0.330588').then(r => r.json());
    });

    it('should return the area name', () => {
        expect(pricesForPosition.areaName).toBe('St Albans');
    });

    it('should return the average price', () => {
        expect(pricesForPosition.averagePrice).toBeGreaterThan(0);
    });

    it('should return the detached average', () => {
        expect(pricesForPosition.detachedAverage).toBeGreaterThan(0);
    });

    it('should return the flat average', () => {
        expect(pricesForPosition.flatAverage).toBeGreaterThan(0);
    });

    it('should return the outcode', () => {
        expect(pricesForPosition.outcode).toBe('AL1');
    });

    it('should return the semi-detached average', () => {
        expect(pricesForPosition.semiDetachedAverage).toBeGreaterThan(0);
    });

    it('should return the terraced average', () => {
        expect(pricesForPosition.terracedAverage).toBeGreaterThan(0);
    });

    it('should return the transaction count', () => {
        expect(pricesForPosition.transactionCount).toBeGreaterThan(0);
    });

    it('should return a 400 when no position is supplied', async () => {
        expect.assertions(1);
        const res = await fetch('http://localhost:5100/prices/position');
        expect(res.status).toBe(400);
    });

    it('should return a 400 when an invalid position is supplied', async () => {
        expect.assertions(1);
        const res = await fetch('http://localhost:5100/prices/position?lat=blah&long=blah');
        expect(res.status).toBe(400);
    });
});