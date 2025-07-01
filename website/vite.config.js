// vite.config.js
import path from 'path';
import { defineConfig } from "vite";
import fs from 'fs';
import usePHP from 'vite-plugin-php';

export default defineConfig({
  plugins: [usePHP({
    entry: [
      "index.php",
      "login_modal.php",
      "require_login.php",
      "src/html/*.php"
    ]
  })],
  build: {
    emptyOutDir: true,
    outDir: 'public'
  },
});