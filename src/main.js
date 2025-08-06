// src/main.js

import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia' // 1. Importar o Pinia
import App from './App.vue'

const app = createApp(App)

app.use(createPinia()) // 2. Ativar o Pinia na aplicação
app.mount('#app')