<template>
    <nav class="navbar">
    <ul v-if="student">
      <li class="nav-item">
        <router-link class="nav-link" to="/">Home</router-link>
      </li>
      <li class="nav-item">
        <router-link class="nav-link" :to="{name: 'NewTicket'}">New Ticket</router-link>
      </li>
      <li class="nav-item">
        <router-link class="nav-link" :to="{name: 'Solutions'}">Solutions</router-link>
      </li>
      <li class="nav-item">
        <router-link class="nav-link" :to="{name: 'MyTickets'}">My Tickets</router-link>
      </li>
    </ul>
    <ul v-if="staff">
      <li class="nav-item">
        <router-link class="nav-link" to="/">Home</router-link>
      </li>
      <li class="nav-item">
        <router-link class="nav-link" :to="{name: 'StaffDashboard'}">Dashboard</router-link>
      </li>
      <li class="nav-item">
        <router-link class="nav-link" :to="{name: 'StaffSolutions'}">My Solutions</router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
import { ref, onMounted } from 'vue';

    export default {
        name: "SideNav",
        setup(){
          const auth = localStorage.getItem('auth')
          const is_logged_in = ref(false)
          const student = ref(false)
          const admin = ref(false)
          const staff = ref(false)

          onMounted(() => {
            window.addEventListener('login-successfull', (e) => {
              if(e.detail.storage == 'student'){
                student.value = true
              }
              else if (e.detail.storage == 'admin'){
                admin.value = true
              }
              else if (e.detail.storage == 'staff'){
                staff.value = true
              }
            })

            window.addEventListener('logout-successfull', (e) => {
              student.value = false
              admin.value = false
              staff.value = false
            })
            if(auth){
              is_logged_in.value = true
              if (auth == 'student'){
                student.value = true
              }
              else if (auth == 'admin'){
                admin.value = true
              }
              else if (auth == 'staff'){
                staff.value = true
              }
            }
            else{
              is_logged_in.value = false
            }
          })
          return {is_logged_in, student, admin, staff}
         
        }
    }
</script>

<style scoped>
nav {
  position: fixed;
  top: 80px;
  left: 0;
  width: 80px;
  height: 100%;
  background-color: #333;
  color: #fff;
  /* padding: 20px; */
}

nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
    padding-left: 0;
    padding-right: 0;
    margin-top: 2rem;
    margin-bottom: 2rem;
    width: 80px;
    text-align: center;
}

.nav-link{
  padding-top: 1.5rem;
    padding-bottom: 1.5rem;
    padding-left: 0;
    padding-right: 0;
    margin-top: 2rem;
    margin-bottom: 2rem;
    width: 80px;
    text-align: center;
}

.nav-item:hover{
    background-color: #2c3e50;
}

.nav-link {
  color: #fff;
  text-decoration: none;
  
  
  
}
nav a {
  font-weight: bold;
  color: #2c3e50;
  /* padding-top: 1.5rem;
  padding-bottom: 1.5rem; */
}

nav a.router-link-exact-active {
  color: #42b983;
}

</style>