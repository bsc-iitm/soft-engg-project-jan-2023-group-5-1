<template>
    <div>
        <h1>FAQ</h1>

        <div v-if="loading" class="load"></div>

        <div class="faq-container" v-show="!loading">
            <div v-for="faq in faq_list" :key="faq.id" class="faq">
                <router-link :to="{ name:'FaqDetails', params: { id: faq.id } }">
                    <div class="title">{{ faq.ticket.title }}</div>
                </router-link>
            
            </div>
        </div>

    </div>
</template>

<script>
    import { ref, inject, onMounted } from 'vue';
    export default {
        name: "Faq",

        setup(){
            const store = inject('store')

            const faq_list = ref([])
            const loading = ref(true)

            const get_faq = async () => {
                const resp = await fetch('http://localhost:5000/ticket/get-all-faqs', {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'accept': 'application/json'
                    }
                })


                const data = await resp.json()
                loading.value = false
                faq_list.value = data
                console.log(data)
            }

            onMounted(() => {
                get_faq()
            })
            
    
            
    
            
    
            
            return { store, faq_list, loading }
             
        }
        
    }
</script>

<style scoped>

.faq-container{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 90%;
    height: 100%;
    
}

.faq-container a{
    text-decoration: none;
    color: black;
}

.title{
    font-size: 1.5rem;
    font-weight: 600;
    margin: 1rem;
}

.faq{
    width: 100%;
    border-bottom: 1px solid black;
    
    display: flex;
    flex-direction: column;
    align-items: left;
    justify-content: left;
    text-align: left;
    margin: 10px auto;
}

.faq:hover{
    background-color: #f2f2f2;
}


</style>