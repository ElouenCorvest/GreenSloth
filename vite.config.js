// vite.config.js
import path from 'path';
import { defineConfig } from "vite";
import fs from 'fs';
import usePHP from 'vite-plugin-php';
import { VitePluginRadar } from 'vite-plugin-radar'

export default defineConfig({
  base: "/",
  plugins: [
    usePHP({
      entry: [
        "index.php",
        "login_modal.php",
        "require_login.php",
        "src/html/*.php"
      ]
    }),
    VitePluginRadar({
      analytics: {
        id: "G-5DRSGHZ07C"
      }
    })
  ],
  build: {
    emptyOutDir: true,
    outDir: 'out'
  },
});