import type { Location } from "./Location";
import type { Settings } from "./Settings";
import type { SSL } from "./SSL";


export type Server = {
    serverName: string;
    locations: Location[];
    listen?: number;
    extraSettings?: Settings;
    ssl: SSL;
    id?: number;
}