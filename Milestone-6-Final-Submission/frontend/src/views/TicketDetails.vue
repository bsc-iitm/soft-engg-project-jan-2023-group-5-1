<template>
    <div class="t-header">
        <div class="issued_by">issued by: {{ticket.issuer.username }} @ {{ ticket.issued_at }}</div>
        <div class="status">{{ ticket.status }}</div>
        <!-- <div class="resolved_by">{{ ticket.resolver.username }} @ {{ ticket.resolved_at }}</div> -->
    </div>
    <div class="new-ticket">
        <h2>Ticket</h2>
        <input type="text" name="title" id="title" :value="ticket.title" readonly>
        
        <QuillEditor 
        read-only="true" 
        style="min-height:200px;" 
        theme="snow" toolbar="minimal" 
        :modules="modules" 
        v-model:content="issue_body" 
        class="quill" 
        content-type="html" 
        ref="issue_editor" />
        
        <one-up-icon class="one-up" @click="one_up" ref="one_up_icon"/>

        <h2>Solution</h2>

        <QuillEditor 
        style="min-height:200px;" 
        theme="snow" toolbar="minimal" 
        :modules="modules" 
        v-model:content="solution_body" 
        :read-only="!staff"
        class="quill" 
        content-type="html" 
        ref="solution_editor" />  

        <div v-if="staff" class="btn-grp">
            <button @click="resolve">Resolve</button>
            <button class="red" @click="reset">Reset</button>
            <button @click="add_faq" class="blue">Add to FAQ</button>
           
        </div>
        <div v-if="can_delete" class="btn-grp">
            
            <button @click="delete_ticket">Delete</button>
          
        </div>

    
    </div>
    
</template>

<script>
    import { QuillEditor } from '@vueup/vue-quill'
    import BlotFormatter from 'quill-blot-formatter'
    import '@vueup/vue-quill/dist/vue-quill.snow.css';
    import { ref, onMounted, computed, onBeforeMount, inject, watch } from 'vue';

    import OneUpIcon from  'vue-material-design-icons/OneUp.vue'
    import { useRoute } from 'vue-router';
    export default {
        name: "TicketDetails",
        components: {
            QuillEditor,
            OneUpIcon
        },
        setup: () => {
            const store = inject('store')
            const modules = {
            name: 'blotFormatter',  
            module: BlotFormatter, 
            }
            const user = store.username

            const route = useRoute()
            const one_up_icon = ref(null)
            const one_up = () => {
                one_up_icon.value.$el.classList.toggle('active')
            }
            const ticket = ref(
                {
                id: 1,
                title: '',
                body: '',
                issued_at: null,
                status: '',
                issuer: {
                    username: '',
                    email: ''},
                resolver: {
                    username: '',
                    email: ''},
                solution: '',
                resolved_at: null,
                user_attachments: [],
                staff_attachments: [],
                one_up: 0
            
            }
            )

            

            const auth = store.auth
            const staff = store.staff

            const issue_body = ref('')  // v-model for issue editor
            const solution_body = ref('')  // v-model for solution editor
            const issue_editor = ref(null)
            const solution_editor = ref(null)
            const can_delete = ref(false)
         
            const id = route.params.id
            const get_ticket = async () => {
                const url = 'http://localhost:5000/ticket/' + id
                const resp = await fetch(url, {
                    method: 'GET',
                    credentials: 'include',
                })

                const data = await resp.json()
                console.log(data)
                ticket.value = data
                

            }

            const resolve = () => {
                const url = 'http://localhost:5000/ticket/resolve/' + id
                fetch(url, {
                    method: 'PUT',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        solution: solution_body.value
                    })
                })
                .then(res => res.json())
                .then(data => {
                    console.log(data)
                })
            }

            const reset = () => {
                solution_editor.value.setHTML('')
            }

            const delete_ticket = () => {
                const url = 'http://localhost:5000/ticket/delete/' + id
                fetch(url, {
                    method: 'DELETE',
                    credentials: 'include',
                })
                .then(res => res.json())
                .then(data => {
                    console.log(data)
                })
            }

            const add_faq = () => {
                const url = 'http://localhost:5000/ticket/add-faq/' + id
                fetch(url, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'Accept': 'application/json',
                    },
                    
                })
                .then(res => res.json())
                .then(data => {
                    console.log(data)
                })
            }

            onBeforeMount(() => {
                console.log('before mount started')
                get_ticket()
                console.log('ticket fetched')
                console.log(ticket.value)
            })
            onMounted(()=>{
                console.log('mount started')
                console.log(ticket.value)
                if (ticket.value.issuer.username == user) {
                    can_delete.value = true
                }
                issue_editor.value.setHTML(ticket.value.body)
                solution_editor.value.setHTML(ticket.value.solution)
            })

            watch(ticket, ()=>{

                issue_editor.value.setHTML(ticket.value.body)
                solution_editor.value.setHTML(ticket.value.solution)
                if (ticket.value.issuer.username == user) {
                    can_delete.value = true
                }
                console.log(staff.value)

            })


          

           

            return { 
                modules,
                issue_editor,
                solution_editor, 
                issue_body,
                solution_body,
                staff,
                resolve,
                reset,
                one_up,
                one_up_icon,
                ticket,
                delete_ticket,
                can_delete,
                add_faq


                
            }
        }
    }
</script>

<style scoped>

.ql-container, .ql-editor {
  min-height: inherit;
}

.t-header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background-color: #fff;
    border-bottom: 1px solid #ddd;
}

.new-ticket{
    max-width: 90%;
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    padding: 2rem;
    text-align: left;
    justify-content: flex-start;
}

.new-ticket label {
    letter-spacing: 1px;
    color: #aaa;
    margin: 25px 0 15px;
    text-transform: uppercase;
    font-weight: bold;
    display: inline-block;
}

.new-ticket input{
    width: 80%;
    display: block;
    padding: 10px 6px;
    /* width: 100%; */
    box-sizing: border-box;
    border: none;
    border-bottom: 1px solid #ddd;
    color: #555;
    margin-bottom: 25px;
}

.new-ticket input[type="text"]{
    text-transform: capitalize;
    font-size: 1.6rem;
}


.new-ticket .quill {
    min-width: 80%;
    min-height: 400px;
}

.new-ticket .btn-grp {
    display: flex;
    flex-wrap: wrap;

}

.new-ticket button{
    background: #2a623d;
    color: white;
    padding: 10px;
    margin: 20px;
    border-radius: 20px;
    border: none;
    width: 200px;
    display: inline-block;
    cursor: pointer;
}

.new-ticket button.red{
    background: red;
    color: white;
    padding: 10px;
    margin: 20px;
    border-radius: 20px;
    border: none;
    width: 200px;
    display: inline-block;
    cursor: pointer;
}

.new-ticket button.blue{
    background: navy;
    color: white;
    padding: 10px;
    margin: 20px;
    border-radius: 20px;
    border: none;
    width: 200px;
    display: inline-block;
    cursor: pointer;
}


</style>