<template>
    <div class="new-ticket">
        <label for="title">Title</label>
        <input type="text" name="title" id="title" v-model="title" placeholder="Subject...">
        <QuillEditor style="min-height:200px;" theme="snow" toolbar="full" :modules="modules" v-model:content="body" placeholder="Body..." class="quill" content-type="html" ref="editor" />
        <div class="btn-grp">
            <button @click="submit">Submit</button>
            <button @click="reset">Reset</button>
            <!-- {{ body }} -->
        </div>
    </div>
    
</template>

<script>
    import { QuillEditor } from '@vueup/vue-quill'
    import BlotFormatter from 'quill-blot-formatter'
    import '@vueup/vue-quill/dist/vue-quill.snow.css';
    import { ref } from 'vue';
    export default {
        name: "NewTicket",
        components: {
            QuillEditor
        },
        setup: () => {
            const modules = {
            name: 'blotFormatter',  
            module: BlotFormatter, 
            }

            const title = ref('')
            const body = ref('')
            const editor = ref(null)

            const reset = () =>{
                title.value = ''
                editor.value.setContents('')
                
            }

            const submit = () => {
                let data = {
                    title: title.value,
                    body: body.value,
                    user_attachments: []
                }
                const url = 'http://localhost:5000/ticket/issue-ticket'
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
                    console.log(data)
                })
            }

            return { modules, title, body , reset, editor, submit}
        }
    }
</script>

<style scoped>

.ql-container, .ql-editor {
  min-height: inherit;
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

.new-ticket button{
    background: #2a623d;
    color: white;
    padding: 10px;
    margin: 20px;
    border-radius: 20px;
    border: none;
    width: 200px;
    display: inline-block;
}
.new-ticket .quill {
    min-width: 80%;
    min-height: 400px;
}

.new-ticket .btn-grp {
    display: flex;
    flex-wrap: wrap;

}

</style>