<template>
    <div v-if="loading" class="load"></div>
    <div v-show="!loading" class="faq">
        <h1>Title: </h1>
        <div class="title" ref="title"></div>
        <h1>Issue: </h1>
        <div class="issue" ref="issue"></div>
        <h1>Solution: </h1>
        <div class="solution" ref="solution"></div>

    </div>
</template>

<script>
    import { ref, inject, onMounted, watch } from 'vue';
    import { useRoute } from 'vue-router';
    
    export default {
        name: "FaqDetails",

        setup(){
            const store = inject('store')
            const route = useRoute()
            const id = route.params.id
            const faq = ref({})
            const loading = ref(true)
            const title = ref(null)
            const issue = ref(null)
            const solution = ref(null)
            const get_faq = async () => {
                const resp = await fetch('http://localhost:5000/ticket/get-faq/' + id, 
                {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                   
                })

                const data = await resp.json()
                loading.value = false
                faq.value = data
                loading.value = false
                
                console.log(data)
            }

            onMounted(() => {
                get_faq()
                
            })

            watch(faq, () => {
                title.value.innerHTML = faq.value.ticket.title
                issue.value.innerHTML = faq.value.ticket.issue
                solution.value.innerHTML = faq.value.ticket.solution

                console.log(faq.value)
            })

            return { store, faq, loading, title, issue, solution }
        }


    }
</script>

<style scoped>

.faq{
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: start;
    justify-content: space-between;
    padding: 20px;
    box-sizing: border-box;
}

</style>