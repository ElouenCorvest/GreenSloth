import { defineConfig } from 'vite';
import { resolve } from 'path';
import { glob } from 'glob';
import virtualHtml from 'vite-plugin-virtual-html';

// 1. Automatically find all your HTML files
const pages = glob.sync('src/html/**/*.html').reduce((acc, file) => {
  // Logic: 'src/html/model_pages/car.html' -> 'model_pages/car'
  const name = file.replace(/^src\/html\/|\.html$/g, '');
  acc[name] = `/${file}`;
  return acc;
}, {});

// 2. Add your root index.html manually if it's not in src/html
pages.index = '/index.html';

export default defineConfig({
  plugins: [
    virtualHtml({
      pages,
      // This makes it so if you visit localhost:5173/ it shows index.html
      indexPage: 'index', 
    }),
  ],
  build: {
    // This plugin automatically handles rollupOptions.input for you!
  }
});