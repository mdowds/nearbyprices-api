import {validationResult} from "express-validator/check";

export function requestLogger(req, res, next) {
    console.log('GET', req.url);
    next();
}

export function sendErrorResponses(req, res, next) {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
    }
    next();
}
