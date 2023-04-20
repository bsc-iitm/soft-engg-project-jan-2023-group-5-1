<template>
    <nav class="navbar">
    <ul v-if="store.student">
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
    <ul v-if="store.staff">
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
import { ref, onMounted, inject } from 'vue';

    export default {
        name: "SideNav",
        setup(){
          const store = inject('store')
          const auth = ref(store.auth)
          const is_logged_in = ref(false)
          const student = ref(store.student)
          const admin = ref(store.admin)
          const staff = ref(store.staff)

          


          
          return {is_logged_in, student, admin, staff, store}
         
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