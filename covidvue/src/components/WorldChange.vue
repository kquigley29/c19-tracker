<template>
    <div>
        <world-data :countryData="chartData"></world-data>
    </div>
</template>

<script>
import WorldData from './Map/WorldData.vue'
    // const {overwrite, getCode} = require('country-list')
    // overwrite([{
    //     code: 'US',
    //     name: 'United States'
    // },
    //     {
    //         code: 'RU',
    //         name: 'Russia'
    //     },
    //     {
    //         code: 'GB',
    //         name: 'United Kingdom'
    //     }
    // ])

export default {
    data(){
        return{
            chartData: {}
        }
    },
    props:{
        countries: Array
    },
    components:{
        WorldData
    }
}
</script>

<style>

</style>