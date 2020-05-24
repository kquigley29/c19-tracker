<template>
    <div>
        <world-data highColor="#860000" lowColor="#548235" :countryData="chartData"></world-data>
    </div>
</template>

<script>
import WorldData from './Map/WorldData.vue'
    const {overwrite, getCode} = require('country-list')
    overwrite([{
        code: 'US',
        name: 'United States'
    },
        {
            code: 'RU',
            name: 'Russia'
        },
        {
            code: 'GB',
            name: 'United Kingdom'
        }
    ])

export default {
    data(){
        return{
            chartData: {}
        }
    },
    props:{
        countries: Object
    },
    components:{
        WorldData
    },
    computed:{
        // chartData: function(){
        //     let data = {}
        //     let keys = this.countries.keys
        //     for(var key in keys){
        //         let name = getCode(key)
        //         let countryData = this.countries[key]
        //         let calc = (countryData[13].total_cases - countryData[7].total_cases) - (countryData[6].total_cases - countryData[0].total_cases)
        //         if(calc < 0){
        //             data[name] = 1
        //         }
        //         else{
        //             data[name] = -1
        //         }
        //     }
        //     console.log(data)
        //     return data
        // }
    },
    watch:{
        countries: function(){
            let data = {}
            let keys = Object.keys(this.countries)
            for(var key of keys){
                let name = getCode(key)
                if(key == "San Marino"){
                    console.log("hello");
                    
                    continue
                }
                //console.log(name)
                let countryData = this.countries[key]
                if(countryData.length < 10){
                    continue
                }
                let calc = (countryData[13].total_cases - countryData[7].total_cases) - (countryData[6].total_cases - countryData[0].total_cases)
                if(calc <= 0){
                    data[name] = -1
                }
                else{
                    data[name] = 1
                }
            }
            //console.log(data)
            this.chartData = data
        }
    }
}
</script>

<style>

</style>