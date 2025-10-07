import type { Server } from "../models/Server";
import SanitizeServer from "../utils/sanatizeServer";
import { ToCamelCase, ToSnakeCase } from "../utils/toCases";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
const URL_API = `${BACKEND_URL}/server/`

type ServerNoID = Omit<Server, "id">;

export interface ResponseError {
  statusCode: number;
  error: any;
}


export function GetAllServers(): Promise<Server[]> {

    return new Promise(async(resolve, reject) => {
        const response = await fetch(URL_API);
        const responseJson = await response.json();
        if (response.ok) {
            const servers = responseJson.map(
                (server: Server) => ToCamelCase(server)
            );
            return resolve(servers);
        }
        reject({
            statusCode: response.status,
            error: responseJson
        });
    })
 
}

export function CreateServer(server: Server): Promise<Server> {
    server = SanitizeServer(server);
    const { id, ...serverNoID }: { id?: number } & ServerNoID = server;
    const serverSnakeCase = ToSnakeCase(serverNoID);

    return new Promise(async(resolve, reject) => {
        const response = await fetch(URL_API, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(serverSnakeCase)
        });
        const responseJson = await response.json();
        if (response.ok) {
            const server = ToCamelCase(responseJson);
           return resolve(server);
        }
        reject({
            statusCode: response.status,
            error: responseJson
        });
    })
}

export function EditServer(server: Server): Promise<Server> {
    const updateUrl = `${URL_API}${server.id}`;
    server = SanitizeServer(server);
    const { id, ...serverNoID }: { id?: number } & ServerNoID = server;
    const serverSnakeCase = ToSnakeCase(serverNoID);

    return new Promise(async(resolve, reject) => {
        const response = await fetch(updateUrl, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(serverSnakeCase)
        });
        const responseJson = await response.json();
        if (response.ok) {
            const server = ToCamelCase(responseJson);
           return resolve(server);
        }
        reject({
            statusCode: response.status,
            error: responseJson
        });
    })
}

export function DeleteServer(id: number): Promise<void> {
    const urlDelete = `${URL_API}${id}`;
    return new Promise(async(resolve, reject) => {
        const response = await fetch(urlDelete, {
            method: "DELETE"
        });
        if (response.ok) return resolve();
        reject({
            statusCode: response.status,
            error: await response.json()
        });
    })
}