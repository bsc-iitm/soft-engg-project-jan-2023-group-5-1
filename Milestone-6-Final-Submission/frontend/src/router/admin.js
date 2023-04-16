import AdminLogin from '../views/admin/AdminLogin.vue'
import AdminRegister from '../views/admin/AdminRegister.vue'

const admin_routes = [{
        path: '/admin/login',
        name: 'AdminLogin',
        component: AdminLogin
    },
    {
        path: '/admin/register',
        name: 'AdminRegister',
        component: AdminRegister
    },
]


export default admin_routes