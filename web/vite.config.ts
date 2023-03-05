import { defineConfig } from 'vite'
import preact from '@preact/preset-vite'
import { vanillaExtractPlugin } from '@vanilla-extract/vite-plugin'

// https://vitejs.dev/config/
export default defineConfig({
  //@ts-ignore idk why
  alias: {
    "react": "preact/compat"
  },
  plugins: [preact(), vanillaExtractPlugin()],

})
