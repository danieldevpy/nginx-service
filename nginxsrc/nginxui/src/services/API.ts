import type { Server } from "../models/Server";


export default class APIBACKEND {
    readonly urlBase: string;

    constructor(path: string) {
        const CUSTOM_URL = import.meta.env.VITE_API_URL;
        this.urlBase = CUSTOM_URL? `${CUSTOM_URL}/${path}/` : `/${path}/`;
    }

    response(fetch: Promise<Response>): Promise<Server> {
        return new Promise(async(resolve, reject) => {
            const response = await fetch;
            const responseJson = await response.json();
            if (response.ok) {
                return resolve(responseJson);
            }
            reject({
                statusCode: response.status,
                error: responseJson
            });
        });
    }
}

