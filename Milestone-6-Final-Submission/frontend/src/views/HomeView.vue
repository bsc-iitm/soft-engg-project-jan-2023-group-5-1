<template>
  <div class="home">
    <div class="header">
      <div class="search_box">
        <input type="search" name="search" id="search" :class="{ active: content }" v-model="search" @keypress.space="get_similar" placeholder="Search...">
        <div :class="{ recom: true, active: content }">
          <ul>

         
              <li v-for="result in search_results" :key="result.id">
                <router-link :to="{ name: 'TicketDetails', params: { id: result.id } }">{{result.title}}</router-link>
              </li>
        

          </ul>
        </div>
      </div>


    </div>
    <div class="faq">

      <Faq />

    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Faq from '@/components/Faq.vue';


import { ref, watch, computed } from 'vue';


export default {
  name: 'HomeView',
  components: {
    Faq
  },
  setup(){
    const search = ref('')
    const search_results = ref([])
    // const terms = ref(0)
    const content = computed(() => {
      if(search_results.value.length > 0){
        return true
      }
      else{
        return false
      }
    })
    const get_similar = async ()=>{
      const resp = await fetch('http://localhost:5000/ticket/get-similar', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: search.value
        })
      })

      const data = await resp.json()
      search_results.value = data
      console.log(data)
    }
   
    watch(search, async (new_term) => {

      // console.log(new_term)
      const len = new_term.length
      if (len === 0){
        search_results.value = []
      }
      
      
      
      

    }) 

    return {
      search,
      search_results,
      content,
      get_similar

    }
  }
}
</script>


<style scoped>

.header{
  height: 50vh;
  width: 96%;
  display: flex;
  justify-content: center;

}

.header input{
  width: 75%;
  height: 60px;
  border-radius: 10px;
  border: 1px #333 solid;
  padding: 10px;
  font-size: 20px;
  position: relative;
}

.search_box{
  position: relative;
  width: 80%;
  height: 60px;
}

.recom{
  position: absolute;
  top: 100%;
  left: 12.5%;
  width: 75%;
  background-color: #fff;
  border: 1px #333 solid;
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;
  z-index: 100;
  display: none;
}

.recom ul{
  list-style: none;
  padding: 5px;
  margin: 0;
  border-bottom: #333 1px solid;
  text-align: left;
  font-size: 1.5rem;
}

.recom li{
  padding: 5px;
  cursor: pointer;
}

.recom li a{
  text-decoration: none;
  color: inherit;
  display: block;
  width: 100%;
  /* color: #333; */
}

.recom li:hover{
  background-color: #333;
  color: #fff;
}

.recom.active{
  display: block;
}

input.active{
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}
</style>
