<template>
    <div class="my-tickets">
        <div class="tickets">
            <div class="ticket" v-for="ticket in tickets" :key="ticket.id">
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

    import { ref, onMounted } from 'vue'


    import Ticket from '../components/Ticket.vue'
    export default {
        name: "MyTickets",
        components: {
            Ticket
        },

        setup(){
            const user = localStorage.getItem('username')
            const tickets = ref([
                
                {
                    id: 1,
                    title: 'Ticket 1',
                    body: 'body',
                    issued_at: new Date(),
                    status: 'Resolved',
                    issuer: {
                        username: 'John Doe',
                        email: ''},
                    resolver: {
                        username: 'Jane Doe',
                        email: ''},
                    solution: 'Solution',
                    resolved_at: new Date(),
                    user_attachments: [],
                    staff_attachments: [],
                    one_up: 10
                }
            ])
                
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
                })
            }

            onMounted(() => {
                get_issues()
            })
            
            return { 
                tickets,
                user
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