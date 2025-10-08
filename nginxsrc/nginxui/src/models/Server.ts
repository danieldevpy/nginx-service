import type { Location } from "./Location";
import type { SSL } from "./SSL";


export type Server = {
    serverName: string;
    locations: Location[];
    ssl: SSL;
    extraSettings: string[];
    listen?: number;
    id?: number;
}