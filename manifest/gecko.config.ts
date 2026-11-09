import { defineManifest } from "@crxjs/vite-plugin";
import packageJson from "../package.json" with { type: "json" };

export default defineManifest({
  manifest_version: 3,
  name: "SamHacker's Browser Homepage",
  version: packageJson.version,
  description:
    "A browser homepage that displays the current time, date, and weather.",

  chrome_url_overrides: {
    newtab: "index.html",
  },

  permissions: ["geolocation"],

  host_permissions: [
    "https://samhacker.xyz/*",
    "https://api.samhacker.xyz/*",
    "https://api.github.com/*",
    "https://api.nlsc.gov.tw/*",
    "http://127.0.0.1:5000/*",
  ],

  browser_specific_settings: {
    gecko: {
      id: "newtab@samhacker.xyz",
      strict_min_version: "142.0",
      update_url:
        "https://github.com/510208/browser-homepage-next/releases/latest/download/updates.json",
      data_collection_permissions: {
        required: ["locationInfo"],
      },
    },
  },

  icons: {
    "48": "extensions/icon48.png",
    "128": "extensions/icon128.png",
  },

  background: {
    scripts: ["src/background/index.ts"],
  },
});
