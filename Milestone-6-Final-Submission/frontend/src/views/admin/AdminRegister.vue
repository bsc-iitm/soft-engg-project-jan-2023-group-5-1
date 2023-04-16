<template>
    <div class="body">
        <div class="student">
            <h1>Admin Sign up</h1>
            <img src="../../../public/img/undraw_security_on_re_e491.svg" alt="">
        </div>
        <div class="box">
            <form @submit.prevent="register">
              <label for="username">Username:</label>
              <input type="text" v-model="username" name="username" required>
  
              <label for="email">Email:</label>
              <input type="email" v-model="email" name="email" required>
              
              <label for="password">Password:</label>
              <input type="password" v-model="password" name="password" required>

             
  
              <center>
                  <button type="submit">Register</button>
  
              </center>
              
            </form>
  
        </div>
    </div>
  </template>


<script>


import { ref } from 'vue';
import { useRouter } from 'vue-router'
  export default {
    setup () {
        const username = ref('')
        const password = ref('')
        const email = ref('')
        const router = useRouter()
        const register = () => {
            const url = 'http://localhost:5000/admin/register'
            let data = {
                username: username.value,
                password: password.value,
                email: email.value
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
                router.push('/admin/login')
            })
        }
    
        return {
            username,
            password,
            email,
            register
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
        height: 320px;
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
    }

</style>