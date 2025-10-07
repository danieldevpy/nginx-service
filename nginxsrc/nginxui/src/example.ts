
export const ServerExample = {
  server_name: "cisbaf.org.br",
  listen: 80,
  extra_settings: null,
  ssl: false,
  locations: [
    {
      path: "/",
      type: "proxy",
      active: true,
      proxy_pass: "https://example.com/",
      redirect_to: null,
      status_code: null,
      root: null,
      rewrite_rule: null,
      last: null,
    },
  ],
  id: 1,
};
