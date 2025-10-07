
export const LocationTypeEnum = {
  PROXY: "proxy",
  REDIRECT: "redirect",
  STATIC: "static",
  REWRITE: "rewrite",
  MAINTENANCE: "maintenance"
} as const;

export type LocationType = typeof LocationTypeEnum[keyof typeof LocationTypeEnum];


export type Location = {
    path: string;
    type: LocationType;
    active?: boolean;
    proxyPass?: string;
    redirectTo?: string;
    status_code?: number;
    root?: string;
    rewriteRule?: string;
    last?: boolean;
}