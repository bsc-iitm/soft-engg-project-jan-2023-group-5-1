<template>
    <div class="my-tickets">
        <div class="tickets">
            <div v-if="loading" class="load"></div>
            <div class="ticket" v-for="ticket in tickets" :key="ticket.id" v-show="!loading">
                <router-link :to="{ name: 'TicketDetails', params: { id: ticket.id } }">
                    <Ticket
                    :id="ticket.id"
                    :title="ticket.title"
                    :status="ticket.is_resolved"
                    :issued_by="ticket.issuer.username"
                    :date_issued="ticket.issued_at" />
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>

    import { ref, onMounted, inject } from 'vue'


    import Ticket from '@/components/Ticket.vue'
    export default {
        name: "MyTickets",
        components: {
            Ticket
        },

        setup(){
            const store = inject('store')
            const user = store.username
            const tickets = ref([])
            const loading = ref(true)
                
            const get_resolves = () => {
                const url = 'http://localhost:5000/ticket/get-all-resolves'
                fetch(url, {
                    method: 'GET',
                    credentials: 'include',
                })
                .then(res => res.json())
                .then(data => {
                    tickets.value.push(...data)
                    loading.value = false
                    // console.log(tickets.value)
                })
            }

            onMounted(() => {
                get_resolves()
            })
            
            return { 
                tickets,
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