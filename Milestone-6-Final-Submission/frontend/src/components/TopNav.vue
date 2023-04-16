<template>
    <div class="nav-container">
      <nav class="navbar">
          <div class="logo">LOGO</div>
          <ul class="navbar-nav">
              <li class="nav-item">
                  <router-link class="nav-link" to="/about"><bell-icon :size="32" /></router-link>
              </li>
              <li class="nav-item">
                  <span @mouseover ="on_subMenu"><account-circle-icon :size="32" /></span>
              </li>
          </ul>
          <div :class="{ submenubox: true, active: subMenu }">
            <div class="sub-menu" @mouseleave="off_subMenu">
              <h3>Abul Aman</h3>
              <ul>
                <li v-if="!student"><router-link :to="{ name: 'StudentLogin' }"> <account-circle-icon /> <span>Sign in as student</span></router-link></li>
                <li v-if="!staff"><router-link :to="{ name: 'StaffLogin' }" > <human-male-board-icon /> <span>Sign in as staff</span></router-link></li>
                <li v-if="!admin"><router-link :to="{ name: 'AdminLogin' }" > <security-icon /> <span>Sign as admin</span></router-link></li>
                <li v-if="user" @click="logout"><logout-icon /> <span>Sign out</span></li>

              </ul>
            </div>
          </div>
        </nav>
    </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import AccountCircleIcon from 'vue-material-design-icons/AccountCircle.vue'
import BellIcon from 'vue-material-design-icons/Bell.vue'
import AccountSchoolIcon from 'vue-material-design-icons/AccountSchool.vue'
import SecurityIcon from 'vue-material-design-icons/Security.vue'
import HumanMaleBoardIcon from 'vue-material-design-icons/HumanMaleBoard.vue'
import LogoutIcon from 'vue-material-design-icons/Logout.vue'
    export default {
        name: "TopNav",
        components: {
          AccountCircleIcon,
          BellIcon,
          AccountSchoolIcon,
          SecurityIcon,
          HumanMaleBoardIcon,
          LogoutIcon
        },
        setup () {
          const router = useRouter()
        const subMenu = ref(false)
        const user = ref(localStorage.getItem('username'))
        const auth = localStorage.getItem('auth')
        const ref_auth = ref(auth)
        const student = computed(() => {
          if(ref_auth == 'student') {
            return true
          }
          else{
            return false
          }
        })

        const staff = computed(() => {
          if(ref_auth == 'staff') {
            return true
          }
          else{
            return false
          }
        })

        const admin = computed(() => {
          if(ref_auth == 'admin') {
            return true
          }
          else{
            return false
          }
        })
        


        const on_subMenu = () => {
          subMenu.value = true
        }
        const off_subMenu = () => {
          subMenu.value = false
        }

        const logout = async () => {
          const url = `http://localhost:5000/${auth}/logout`
          const resp = await fetch(url, {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
            },
            credentials: 'include'
          })
          const data = await resp.json()
          console.log(data)
          localStorage.removeItem('username')
          localStorage.removeItem('auth')
          window.dispatchEvent(new CustomEvent('logout-successfull', {
                    detail: {
                        storage: localStorage.getItem('auth')
                    }
                    }))
          ref_auth.value = null
          user.value = null
          router.push('/')
        }
      
        return {
          subMenu, on_subMenu, off_subMenu, user, student, staff, admin, logout
        }
      }
    }
      
    
</script>

<style scoped>

.submenubox{
  position: absolute;
  top: 105%;
  right: 1%;
  padding: 10px;
  max-height: 0px;
  overflow-y: hidden;
  overflow-x: hidden;
  border-radius: 5px;
  /* display: none; */
  /* transition: max-height 0.5s ease-in-out; */
  /* transition: all 0.5s ease-in-out; */


  
}

.submenubox.active{
  max-height: 400px;
  border: 1px #333 solid;
  background-color: #333;
  /* display: block; */
}
.sub-menu{
  color: white;
  /* border: 1px green solid; */
  border-radius: 5px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  text-align: left;
}

.sub-menu ul{
  text-decoration: none;
  list-style-type: none;
  display: flex;
  flex-direction: column;
  color: white;
  padding-left: 0;
  
  /* border-bottom: 1px #2c3e50 solid; */
}

.sub-menu ul li{
  display: flex;
  justify-content: left;
}

.sub-menu ul li a{
  text-decoration: none;
  color: white;
  padding: 5px;
  display: flex;
  justify-content: left;
  text-align: justify;
  width: 100%;
}

.sub-menu ul li a:hover{
  outline: 1px white solid;
  border-radius: 5px;
}

.sub-menu ul li a span{
  margin-left: 10px;
}

.nav-container {
  position: relative;
  padding: 0%;
}
nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 40px;
  background-color: #333;
  color: #fff;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  margin-bottom: 60px;
  z-index: 1000;
}

nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: row;
}

nav ul li {
  padding: 10px;
}

nav ul li span {
  color: #fff;
  text-decoration: none;
  font-weight: bold;
  cursor: pointer;
}

nav ul li a {
  color: #fff;
  text-decoration: none;
}
nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
.logo{
    display: flex;
    justify-content: space-around;
    margin-left: 5rem;
    font-size: 2rem;
}
</style>