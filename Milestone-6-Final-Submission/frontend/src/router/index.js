import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MyTickets from '../views/MyTickets.vue'
import NewTicket from '../views/NewTicket.vue'
import TicketDetails from '../views/TicketDetails.vue'
import Solutions from '../views/Solutions.vue'
import student_routes from './student'
import admin_routes from './admin'
import staff_routes from './staff'

const routes = [{
        path: '/',
        name: 'home',
        component: HomeView
    },
    {
        path: '/about',
        name: 'about',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
            import ( /* webpackChunkName: "about" */ '../views/AboutView.vue')
    },
    {
        path: '/new-ticket',
        name: 'NewTicket',
        component: NewTicket
    },
    {
        path: '/solutions',
        name: 'Solutions',
        component: Solutions
    },
    {
        path: '/my-tickets',
        name: 'MyTickets',
        component: MyTickets,

    },

    {
        path: '/tickets/:id',
        name: 'TicketDetails',
        component: TicketDetails,
        props: true
    },

    ...staff_routes,
    ...student_routes,
    ...admin_routes





]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router