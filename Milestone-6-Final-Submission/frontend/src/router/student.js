import StudentLogin from '../views/StudentLogin.vue'
import StudentRegister from '../views/StudentRegister.vue'


const student_routes = [{
        path: '/student/login',
        name: 'StudentLogin',
        component: StudentLogin
    },
    {
        path: '/student/register',
        name: 'StudentRegister',
        component: StudentRegister
    },
]

export default student_routes