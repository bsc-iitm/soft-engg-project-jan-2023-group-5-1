<template>
    <div class="my-tickets">
        <div class="tickets">
            <div v-if="loading" class="load"></div>
            <div v-show="!loading" class="ticket" v-for="ticket in solved" :key="ticket.id">
                <router-link :to="{ name: 'TicketDetails', params: { id: ticket.id } }">
                    <Ticket
                    :id="ticket.id"
                    :title="ticket.title"
                    :status="ticket.is_resolved"
                    :issued_by="ticket.issuer.username"
                    :date_issued = "ticket.issued_at" />
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>

    import { ref, onMounted, inject, computed } from 'vue'


    import Ticket from '../components/Ticket.vue'
    export default {
        name: "MyTickets",
        components: {
            Ticket
        },

        setup(){
            const store = inject('store')
            const user = store.username
            const loading = ref(true)
            const tickets = ref([])
                
            const get_issues = () => {
                const url = 'http://localhost:5000/ticket/get-all-issues'
                fetch(url, {
                    method: 'GET',
                    credentials: 'include',
                })
                .then(res => res.json())
                .then(data => {
                    // console.log(data)
                    tickets.value.push(...data)
                    loading.value = false
                })
            }

            onMounted(() => {
                get_issues()
            })


            const solved = computed(() => {
                return tickets.value.filter(ticket => ticket.is_resolved == true)
            })
            
            
            return { 
                solved,
                user,
                loading
             }
        }
        
    }
</script>

<style scoped>

.ticket a {
    text-decoration: none;
    color: black;
}

</style>