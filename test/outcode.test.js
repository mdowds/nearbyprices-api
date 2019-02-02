const fetch = require('node-fetch');

let pricesForOutcode;

describe('GET /prices/outcode', () => {
    beforeAll(async () => {
        pricesForOutcode = await fetch('http://localhost:5100/prices/outcode/AL1').then(r => r.json());
    });

    it('should return the area name', () => {
        expect(pricesForOutcode.areaName).toBe('St Albans');
    });

    it('should return the average price', () => {
        expect(pricesForOutcode.averagePrice).toBeGreaterThan(0);
    });

    it('should return the detached average', () => {
        expect(pricesForOutcode.detachedAverage).toBeGreaterThan(0);
    });

    it('should return the flat average', () => {
        expect(pricesForOutcode.flatAverage).toBeGreaterThan(0);
    });

    it('should return the outcode', () => {
        expect(pricesForOutcode.outcode).toBe('AL1');
    });

    it('should return the semi-detached average', () => {
        expect(pricesForOutcode.semiDetachedAverage).toBeGreaterThan(0);
    });

    it('should return the terraced average', () => {
        expect(pricesForOutcode.terracedAverage).toBeGreaterThan(0);
    });

    it('should return the transaction count', () => {
        expect(pricesForOutcode.transactionCount).toBeGreaterThan(0);
    });

    it('should return a 400 if an invalid outcode is supplied', async () => {
        expect.assertions(1);
        const res = await fetch('http://localhost:5100/prices/outcode/01');
        expect(res.status).toBe(400);
    });
});