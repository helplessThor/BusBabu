import { defineConfig } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['busbabu.svg', 'busdata.json'],
      manifest: {
        name: 'BusBabu Kolkata',
        short_name: 'BusBabu',
        description: 'Kolkata local bus route finder and navigation app.',
        theme_color: '#f9d342',
        background_color: '#1a1a1a',
        display: 'standalone',
        icons: [
          {
            src: '/img/busbabu.png',
            sizes: '512x512',
            type: 'image/png'
          },
          {
            src: '/img/busbabu.svg',
            sizes: '512x512',
            type: 'image/svg+xml'
          }
        ]
      }
    })
  ]
});
