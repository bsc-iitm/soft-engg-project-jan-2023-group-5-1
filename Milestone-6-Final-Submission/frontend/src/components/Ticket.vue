<template>
    <div class="ticket">
        <div class="header">
            <div class="title">{{ ticket.title }}</div>
            <div class="status">{{ ticket.status }}</div>
        </div>
        <div class="footer">
            <div class="issued_by">issued by: {{ ticket.issued_by }} @ {{ ticket.date_issued }}</div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue'
export default {
    props: {
        id: Number,
        title : String,
        status: Boolean,
        issued_by: String,
        date_issued: String,

    },
    setup (props) {
        const ticket = ref({
            id: props.id,
            title: props.title,
            status: props.status ? 'Resolved' : 'Unresolved',
            issued_by: props.issued_by,
            date_issued: props.date_issued,

        })

        return {
            ticket
        }
    }
}
</script>

<style scoped>

.ticket {
    max-height: 200px;
    width: calc(100% - 30px);
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0,0,0,0.2);
    margin: 15px auto;
    padding: 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;

}

.ticket:hover {
    box-shadow: 0 0 10px rgba(0,0,0,0.4);
}

.ticket .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.ticket .header .title {
    font-size: 1.5rem;
    font-weight: bold;
}

.ticket .header .status {
    font-size: 1.2rem;
    font-weight: bold;
    color: #2a623d;
    margin-left: 10px;
}



.ticket .footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.ticket .footer .issued_by {
    font-size: 0.9rem;
    color: gray;
    font-style: italic;
}

.ticket .footer .resolved_by {
    font-size: 0.9rem;
    color: gray;
    font-style: italic;
}


</style>