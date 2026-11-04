import { mkdir, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import type { Plugin } from "vite";

interface FirefoxUpdateOptions {
  addonId: string;
  version: string;
  updateLink: string;
}

export function firefoxUpdate(options: FirefoxUpdateOptions): Plugin {
  return {
    name: "firefox-update-manifest",
    apply: "build",

    async writeBundle() {
      const { addonId, version, updateLink } = options;

      if (!addonId || !version || !updateLink) {
        throw new Error("[firefox-update] Missing required options.");
      }

      const updates = {
        addons: {
          [addonId]: {
            updates: [
              {
                version,
                update_link: updateLink,
              },
            ],
          },
        },
      };

      const outputDir = resolve(process.cwd(), "release");

      await mkdir(outputDir, { recursive: true });

      await writeFile(
        resolve(outputDir, "updates.json"),
        JSON.stringify(updates, null, 4),
        "utf-8",
      );
    },
  };
}
