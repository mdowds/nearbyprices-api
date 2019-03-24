import {Firestore} from "@google-cloud/firestore";
import * as express from 'express';
import cors = require('cors');
import {check, validationResult} from "express-validator/check";

import pricesForOutcode from "./src/outcode";
import pricesForPosition from "./position";
import {validateLatitude, validateLongitude} from "./src/validate";
import {requestLogger, sendErrorResponses} from "./src/middleware";

const server = express();
const port = process.env.PORT || 5100;

server.use(cors({origin: /mdowds\.com$/}));

const db = new Firestore({
    projectId: process.env.GCLOUD_PROJECT_ID,
    timestampsInSnapshots: true
});
if (process.env.GCLOUD_KEY_FILE) db.settings({keyFilename: process.env.GCLOUD_KEY_FILE});
if (process.env.GCLOUD_PROJECT_ID && process.env.GCLOUD_SA_KEY) db.settings({
    credentials: {
        client_email: process.env.GCLOUD_CLIENT_EMAIL,
        private_key: JSON.parse(`"${process.env.GCLOUD_SA_KEY}"`)
    }
});

server.use(requestLogger);

server.get('/prices/outcode/:outcode',
    check('outcode').isPostalCode('GB'),
    sendErrorResponses,
    (req, res) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }

        pricesForOutcode(db, req.params.outcode).then(output => res.send(output));
    }
);

server.get('/prices/position',
    [check('lat').toFloat().custom(validateLatitude), check('long').toFloat().custom(validateLongitude)],
    sendErrorResponses,
    (req, res) => {
        pricesForPosition(db, {lat: req.query.lat, long: req.query.long}).then(output => res.send(output));
    }
);

server.listen(port, () => console.log(`Server listening on port ${port}`));
