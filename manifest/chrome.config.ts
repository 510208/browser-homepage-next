import { defineManifest } from "@crxjs/vite-plugin";

export default defineManifest({
  manifest_version: 3,
  name: "SamHacker's Browser Homepage",
  version: "1.0.0",
  description: "A browser homepage that displays the current time, date, and weather.",

  key: "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuNKoyClnilHWnpyV9Zlnbvq1sF8FJ2riC7Qq/xqKRVY2ZaarvaoRdYw/hk/qSo8P7pQJFbK/12qYCEaIqrAgS/Ry5SVsQSQUffg3D9xYDS5qHpFzrGqBPNfOWysmf1kYwStOMuTmdC4d4o9xduDDtLdymPS1kEFnW7w7n0NLFRdRnWeiAsDdY8NswXU5ssO0R3T5iPXxZivmTu37Esu8PoHumPCExTbLXI2do1/FGlC1Ap8qstapMEuHeyua5RME8YakWWDTsyPCu/eI+ZGDIv5BxuAwHoiv4+kn+kHU4zPMWGqPYZLXn06lpxolf1ESoKWpF8K8ZedRESSjg8yOhwIDAQAB",

  chrome_url_overrides: {
    newtab: "index.html",
  },

  permissions: ["declarativeNetRequest", "geolocation"],
  host_permissions: ["https://samhacker.xyz/*", "https://api.samhacker.xyz/*"],
  declarative_net_request: {
    rule_resources: [
      {
        id: "ruleset_cors",
        enabled: true,
        path: "extensions/rules.json",
      },
    ],
  },

  browser_specific_settings: {
    gecko: {
      id: "newtab@samhacker.xyz",
    },
  },

  icons: {
    "48": "extensions/icon48.png",
    "128": "extensions/icon128.png",
  },
});
