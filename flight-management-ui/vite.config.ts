import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
port: 5173, cors: { origin: ['nozomi.proxy.rlwy.net:17971','http://metro.proxy.rlwy.net:12922', 'http://localhost:5173', 'http://127.0.0.1:5173','http://127.0.0.1:5555','http://127.0.0.1:5555','http://127.0.0.1:8000','http://127.0.0.1:8001','http://localhost:8000','http://localhost:8001'], methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'], credentials: true } } })
