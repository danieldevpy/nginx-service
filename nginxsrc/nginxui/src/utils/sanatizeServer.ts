import { type Location, LocationTypeEnum } from "../models/Location";
import type { Server } from "../models/Server";

function normalizeLocation(location: Location): Location {
  const baseLocation = {
    path: location.path,
    type: location.type,
    active: location.active ?? true,
  };

  switch (location.type) {
    case LocationTypeEnum.PROXY:
      return {
        ...baseLocation,
        proxyPass: location.proxyPass ?? '',
        redirectTo: undefined,
        status_code: undefined,
        rewriteRule: undefined
      };

    case LocationTypeEnum.REDIRECT:
      return {
        ...baseLocation,
        proxyPass: undefined,
        redirectTo: location.redirectTo ?? '',
        status_code: location.status_code ?? 302,
        root: undefined,
        rewriteRule: undefined
      };

    case LocationTypeEnum.STATIC:
      return {
        ...baseLocation,
        proxyPass: undefined,
        redirectTo: undefined,
        status_code: undefined,
        root: location.root ?? '',
        rewriteRule: undefined
      };

    case LocationTypeEnum.REWRITE:
      return {
        ...baseLocation,
        proxyPass: undefined,
        redirectTo: undefined,
        status_code: undefined,
        root: undefined,
        rewriteRule: location.rewriteRule ?? ''
      };

    case LocationTypeEnum.MAINTENANCE:
      return {
        ...baseLocation,
        proxyPass: undefined,
        redirectTo: undefined,
        status_code: undefined,
        root: undefined,
        rewriteRule: undefined
      };

    default:
      // Fallback para tipos desconhecidos
      const exhaustiveCheck: never = location.type;
      throw new Error(`Tipo de location desconhecido: ${exhaustiveCheck}`);
  }
}

export default function SanitizeServer(server: Server): Server {
  return {
    ...server,
    locations: server.locations.map(location => normalizeLocation(location))
  };
}