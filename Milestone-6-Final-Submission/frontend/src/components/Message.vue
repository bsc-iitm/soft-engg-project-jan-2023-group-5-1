<template>
    <div class="message">
        <span>{{ message }}</span>
    </div>
</template>

<script>
    import { ref } from 'vue'
    export default {
        name: "Message",
        props: {
            message: {
                type: String,
                required: true
            },
            type: {
                type: 'success' | 'error' | 'warning' | 'info',
                required: true
            }
        },
        setup(props){
            const message = ref(props.message)
            const type = ref(props.type)
            return {
                message,
                type
            }
        }
    }
</script>

<style scoped>

.message{
    width: 250px;
    height: 50px;
    position: absolute;
    top: 125px;
    left: calc(50% - 125px);
}

.message span {
    display: block;
    width: 100%;
    height: 100%;
    background-color: #f5f5f5;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0,0,0,0.2);
    padding: 10px;
    text-align: center;
    line-height: 30px;
}

</style>