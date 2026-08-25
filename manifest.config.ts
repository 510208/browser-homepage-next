import { defineManifest } from "@crxjs/vite-plugin";

export default defineManifest({
  manifest_version: 3,
  name: "SamHacker's Browser Homepage",
  version: "1.0.0",
  chrome_url_overrides: {
    newtab: "index.html",
  },
  permissions: ["declarativeNetRequest", "geolocation"],
  host_permissions: ["https://samhacker.xyz*"],
  declarative_net_request: {
    rule_resources: [
      {
        id: "ruleset_cors",
        enabled: true,
        path: "rules.json",
      },
    ],
  },
});