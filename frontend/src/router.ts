import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import Login from "./pages/Login.vue"
import Home from "./pages/Home.vue"
import Dashboard from './pages/Dashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      component: Login
    },
    {
      path: '/',
      component: Home,
      children:[
        {
          path: "/dashboard",
          component:Dashboard
        }
      ]
    },
  ]
})

export default router