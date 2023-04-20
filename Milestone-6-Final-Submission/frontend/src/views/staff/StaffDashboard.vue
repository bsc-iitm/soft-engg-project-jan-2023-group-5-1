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
                    :date_issued = "ticket.issued_at" />
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>


    import Ticket from '@/components/Ticket.vue';
    import { ref, onMounted, onBeforeMount } from 'vue';
    export default {
        name: "StaffDashboard",
        components: {
            Ticket
        },
        setup(){

            const tickets = ref([])
            const loading = ref(true)
            const get_tickets = () => {
                const url = 'http://localhost:5000/ticket'
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
            onBeforeMount(()=>{
                get_tickets()
            })

            return {
                tickets,
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