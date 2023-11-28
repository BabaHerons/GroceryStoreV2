import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from "./router.ts"
import AdminDashVue from './components/AdminDash.vue'
import UserDashVue from './components/UserDash.vue'
import SMDashVue from './components/SMDash.vue'
import NavbarVue from './components/Navbar.vue'

const app = createApp(App)

app.component("NavbarVue", NavbarVue)
app.component("AdminDashVue",AdminDashVue)
app.component("UserDashVue",UserDashVue)
app.component("SMDashVue", SMDashVue)

app.use(router)
app.mount("#app")
