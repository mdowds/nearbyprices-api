import Firestore = FirebaseFirestore.Firestore;
import {PricesForOutcode} from "./types";

export default async function pricesForOutcode(db: Firestore, outcode: string): Promise<PricesForOutcode> {
    const outcodeRef = db.collection('outcodes').doc(outcode);

    const pricesForOutcode = await outcodeRef.get();
    return pricesForOutcode.data() as PricesForOutcode;
}