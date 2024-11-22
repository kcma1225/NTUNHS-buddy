import { createApp } from 'vue';
import App from '../../App.vue';

export function initializeApp() {
  createApp(App).mount('#app');
}
