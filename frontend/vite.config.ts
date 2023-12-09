import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      injectRegister: 'auto',
      workbox: {
        cleanupOutdatedCaches: false,
        globPatterns: ['**/*.{js,css,html,ico,png,svg,json,vue,txt,woff2}']
     },
      manifest:{
        name:"Grocery Store",
        short_name:"GSV2",
        description:"A store for all your daily needs.",
        icons: [
          {
            src:"/vite.svg",
            sizes: "512x512",
            type:"image/svg+xml",
            purpose:"any maskable"
          }
        ]
      }
    })
  ],
})
