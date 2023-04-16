import StaffLogin from '../views/staff/StaffLogin.vue'
import StaffSolutions from '../views/staff/StaffSolutions.vue'
import StaffDashboard from '../views/staff/StaffDashboard.vue'
import StaffRegister from '../views/staff/StaffRegister.vue'


const staff_routes = [{
        path: '/staff/login',
        name: 'StaffLogin',
        component: StaffLogin
    },
    {
        path: '/staff/register',
        name: 'StaffRegister',
        component: StaffRegister
    },
    {
        path: '/staff/my-solutions',
        name: 'StaffSolutions',
        component: StaffSolutions
    },
    {
        path: '/staff/dashboard',
        name: 'StaffDashboard',
        component: StaffDashboard
    }
]

export default staff_routes