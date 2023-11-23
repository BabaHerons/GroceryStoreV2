import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import Login from "./components/Login.vue"
import Home from "./components/Home.vue"
import Dashboard from './components/Dashboard.vue'

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