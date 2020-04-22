<template>
    <div>
        <p>
            Confirmed: {{country.total_cases}}
        </p>
        <p class="">
            Deaths: {{country.total_deaths}}
        </p>
        <p class="">
            Tests: {{country.total_tests}}
        </p>
        <p v-for="date in countryHistory" v-bind:key="date.id">
            {{date.date}}
        </p>
    </div>
</template>

<script>

//THIS COMPONENT IS VERY MUCH WIP
import CountryGraph from "./CountryGraph.vue"
import axios from 'axios'

export default {
    data() {
        return{
            countryHistory: []
        }
    },
    components:{
        CountryGraph
    },
    name: "CountryData",
    props:{
        country: Object
    },
    created(){
        console.log("getting data for".concat(this.country.name));
        let baseUrl = "https://keane.pythonanywhere.com/history/"
        axios.get(baseUrl.concat(this.country.name))
        .then(res => {
            this.countryHistory = res.data
            console.log("Got data for ".concat(this.country.name));
            
        })
    }
}
</script>

<style scoped>

</style>