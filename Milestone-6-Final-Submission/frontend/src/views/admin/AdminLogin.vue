<template>
    <div class="body">
        <div class="student">
            <h1>Admin Login</h1>
            <img src="../../../public/img/undraw_security_on_re_e491.svg" alt="">
        </div>
        <div class="box">
            <form @submit.prevent="login">
              <label for="username">Username:</label>
              <input type="text" v-model="username" name="username" required>
  
              <label for="password">Password:</label>
              <input type="password" v-model="password" name="password" required>
  
              <center>
                  <button type="submit">Log in</button>
  
              </center>
              
            </form>
  
        </div>
    </div>
  </template>


<script>


import { ref, inject } from 'vue';
import jwt_decode from "jwt-decode";
  export default {
    setup () {
        const store = inject('store')
        const username = ref('')
        const password = ref('')
        const login = () => {
            const url = 'http://localhost:5000/admin/login'
            let data = {
                username: username.value,
                password: password.value
            }

            fetch(url, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(res => res.json())
            .then(data => {
                var decoded = jwt_decode(data.access_token);
                console.log(decoded)
                store.auth = decoded.auth_level
                store.username = decoded.username
                store.student = false
                store.staff = false
                store.admin = true
                localStorage.setItem('auth', decoded.auth_level)
                localStorage.setItem('username', decoded.username)
                window.dispatchEvent(new CustomEvent('login-successfull', {
                    detail: {
                        storage: localStorage.getItem('auth')
                    }
                    }))
                router.push('/')
            })
        }
    
        return {
            username,
            password,
            login
        }
    }
  }
</script>





<style scoped>  

    .student {
        display: flex;
        flex-direction: column;
    }

    .student img{
        max-width: 450px;
    }


    .body{
        background-color: #f5f5f5;
        height: 82vh;
        display: flex;
        justify-content: center;
        overflow: hidden;
        margin-top: 0;
    }

    .body h1{
        margin: auto;
    }

    .box{
        width: 420px;
        height: 260px;
        margin: auto;
        background-color: white;
        text-align: left;
        padding: 30px;
        border-radius: 10px;
        display: flex;
        justify-content: center;
    }

    .box form{
        width: 100%;
        max-height: 200px;
        margin: 0 auto;
    }
    label{
        letter-spacing: 1px;
        color: #aaa;
        margin: 25px 0 15px;
        text-transform: uppercase;
        font-weight: bold;
        display: inline-block;
    }
    input{
        display: block;
        padding: 10px 6px;
        width: 100%;
        box-sizing: border-box;
        border: none;
        border-bottom: 1px solid #ddd;
        color: #555;
    }
    button{
        background: #2a623d;
        color: white;
        padding: 10px;
        margin: 20px;
        border-radius: 20px;
        border: none;
        min-width: 200px;
        cursor: pointer;
    }

</style>