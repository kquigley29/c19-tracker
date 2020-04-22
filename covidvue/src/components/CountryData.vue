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
        <country-graph/>
    </div>
</template>

<script>
//THIS COMPONENT IS VERY MUCH WIP
import CountryGraph from "./CountryGraph.vue"
export default {
    components:{
        CountryGraph
    },
    name: "CountryData",
    props:{
        country: Object
    }
}
</script>

<style scoped>

</style>