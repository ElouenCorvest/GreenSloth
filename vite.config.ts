import { defineConfig } from 'vite';
import { resolve } from 'path';
import fs from 'fs';

/**
 * CONFIGURATION
 */
const GOOGLE_TAG_ID = 'G-XXXXXXXXXX'; // Replace with your actual ID
const IGNORED_SRC_DIRS = ['ignored-dir']; // Folders to ignore inside src/html/
const EXCLUDE_PUBLIC_DIRS = ['simulations/python']; // Folders to ignore inside public/

/**
 * Helper to get all HTML files in src/html
 */
function getHtmlEntries(dir: string) {
  const entries: Record<string, string> = {};
  if (!fs.existsSync(dir)) return entries;

  const walk = (currentDir: string) => {
    const files = fs.readdirSync(currentDir);
    files.forEach((file) => {
      const filePath = resolve(currentDir, file);
      const isDirectory = fs.statSync(filePath).isDirectory();
      
      if (isDirectory && IGNORED_SRC_DIRS.includes(file)) {
        return;
      }

      if (isDirectory) {
        walk(filePath);
      } else if (file.endsWith('.html')) {
        const relativePath = filePath.replace(resolve(__dirname, 'src/html'), '').replace(/^\//, '');
        const name = relativePath.replace(/\.html$/, '');
        entries[name] = filePath;
      }
    });
  };

  walk(dir);
  return entries;
}

export default defineConfig({
  root: '.',
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        ...getHtmlEntries(resolve(__dirname, 'src/html')),
      },
    },
  },
  plugins: [
    {
      name: 'google-tag-injector',
      transformIndexHtml(html) {
        if (!GOOGLE_TAG_ID || GOOGLE_TAG_ID === 'G-XXXXXXXXXX') return html;

        const googleTagScript = `
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=${GOOGLE_TAG_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', '${GOOGLE_TAG_ID}');
    </script>
        `;
        
        return html.replace('<head>', `<head>${googleTagScript}`);
      }
    },
    {
      name: 'html-flatten-and-public-filter',
      closeBundle() {
        const distDir = resolve(__dirname, 'dist');
        const srcHtmlDist = resolve(distDir, 'src/html');
        const publicDir = resolve(__dirname, 'public');

        // 1. Flatten HTML files from src/html
        if (fs.existsSync(srcHtmlDist)) {
          const moveFiles = (currentDir: string, targetDir: string) => {
            if (!fs.existsSync(targetDir)) fs.mkdirSync(targetDir, { recursive: true });
            const files = fs.readdirSync(currentDir);
            
            files.forEach((file) => {
              const currentPath = resolve(currentDir, file);
              const targetPath = resolve(targetDir, file);
              
              if (fs.statSync(currentPath).isDirectory()) {
                moveFiles(currentPath, targetPath);
              } else {
                fs.renameSync(currentPath, targetPath);
              }
            });
          };
          
          moveFiles(srcHtmlDist, distDir);
          fs.rmSync(resolve(distDir, 'src'), { recursive: true, force: true });
        }

        // 2. Remove excluded directories from public that Vite might have copied
        EXCLUDE_PUBLIC_DIRS.forEach(dirName => {
          const targetPath = resolve(distDir, dirName);
          if (fs.existsSync(targetPath)) {
            fs.rmSync(targetPath, { recursive: true, force: true });
          }
        });
      }
    },
    {
      name: 'dev-server-rewrite',
      configureServer(server) {
        server.middlewares.use((req, res, next) => {
          const url = req.url || '';
          if (url.includes('.') && !url.endsWith('.html')) return next();
          
          let cleanPath = url.split('?')[0].split('#')[0];
          if (cleanPath.endsWith('/')) cleanPath += 'index';
          if (cleanPath.startsWith('/')) cleanPath = cleanPath.slice(1);
          if (cleanPath === '' || cleanPath === 'index') return next();

          // Check if it's in an ignored src directory
          const pathParts = cleanPath.split('/');
          if (pathParts.length > 0 && IGNORED_SRC_DIRS.includes(pathParts[0])) {
            return next();
          }

          const htmlFile = cleanPath.endsWith('.html') ? cleanPath : `${cleanPath}.html`;
          const fullPath = resolve(__dirname, 'src/html', htmlFile);

          if (fs.existsSync(fullPath)) {
            req.url = `/src/html/${htmlFile}`;
          }
          next();
        });
      },
    },
    {
      name: 'fix-html-links',
      transformIndexHtml(html) {
        return html.replace(/\/src\/html\//g, '/');
      }
    }
  ],
});