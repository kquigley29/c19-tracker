<template>
    <div>
        <!-- <p>
            Confirmed: {{country.total_cases}}
        </p>
        <p class="">
            Deaths: {{country.total_deaths}}
        </p>
        <p class="">
            Tests: {{country.total_tests}}
        </p> -->
        <b-card no-body>
            <b-tabs no-fade card>
                <b-tab no-body title="Cases">
                    <div class="text-center">
                    <b-spinner v-if="!loaded"></b-spinner>
                    <country-graph v-if="casesData != null" :chart-data="casesData"/>
                    </div>
                </b-tab>
                <b-tab no-body title="Deaths">
                    <div class="text-center">
                    <b-spinner v-if="!loaded"></b-spinner>
                    <country-graph v-if="deathsData != null" :chart-data="deathsData"/>
                    </div>
                </b-tab>
                <b-tab no-body title="Tests">
                    <div class="text-center">
                    <b-spinner v-if="!loaded"></b-spinner>
                    <country-graph :options="options" v-if="testsData != null" :chart-data="testsData"/>
                    </div>
                </b-tab>
            </b-tabs>
            <b-dd id="dateDropdown" :text="timePeriod" class="m-md-2">
                <b-dropdown-item-button @click='setTime("week")'>Week</b-dropdown-item-button>
                <b-dropdown-item-button @click='setTime("month")'>Month</b-dropdown-item-button>
                <b-dropdown-item-button @click='setTime("all")'>All Data</b-dropdown-item-button>
            </b-dd>
        </b-card>
    </div>
</template>

<script>

//THIS COMPONENT IS VERY MUCH WIP
import CountryGraph from "./CountryGraph.vue"
import axios from 'axios'

export default {
    data() {
        return{
            options:{
                scales:{
                    yAxes:[{
                        type: 'logarithmic'
                    }]
                }
            },
            timePeriod: "Month",
            countryHistory: [],
            loaded: false,
            casesData: null,
            deathsData: null,
            testsData: null
        }
    },
    components:{
        CountryGraph
    },
    name: "CountryData",
    props:{
        country: Object
    },
    computed:{
        chartData: function(){
            return this.generateChartData(this.countryHistory, 'total_cases', 7)
        }
    },
    created(){
        //console.log("getting data for".concat(this.country.name));
        let baseUrl = "https://keane.pythonanywhere.com/history/"
        axios.get(baseUrl.concat(this.country.name))
        .then(res => {
            this.countryHistory = res.data
            this.loaded = true
            this.casesData = this.generateChartData(this.countryHistory, 'total_cases', 30)
            this.deathsData = this.generateChartData(this.countryHistory, 'total_deaths', 30)
            this.testsData = this.generateChartData(this.countryHistory, 'total_tests', 30)
        })
    },
    methods:{
        setTime(time){
            let num = this.countryHistory.length
            switch(time){
                
                case "week":
                    this.casesData = this.generateChartData(this.countryHistory, 'total_cases', 7)
                    this.deathsData = this.generateChartData(this.countryHistory, 'total_deaths', 7)
                    this.testsData = this.generateChartData(this.countryHistory, 'total_tests', 7)
                    this.timePeriod = "Week"
                    break;
                case "month":
                    this.casesData = this.generateChartData(this.countryHistory, 'total_cases', 30)
                    this.deathsData = this.generateChartData(this.countryHistory, 'total_deaths', 30)
                    this.testsData = this.generateChartData(this.countryHistory, 'total_tests', 30)
                    this.timePeriod = "Month"
                    break;
                case "all":
                    
                    this.casesData = this.generateChartData(this.countryHistory, 'total_cases', num)
                    this.deathsData = this.generateChartData(this.countryHistory, 'total_deaths', num)
                    this.testsData = this.generateChartData(this.countryHistory, 'total_tests', num)
                    this.timePeriod = "All"
                    break;
                default:
                    break;
            }
        },
        generateChartData(placeHistory, field, numDays){
            let label = ""
            switch(field){
                case "total_cases":
                    label = "Total Cases"
                    break;
                case "total_deaths":
                    label = "Total Deaths"
                    break;
                case "total_tests":
                    label = "Total Tests"
                    break;
                default:
                    label = "Data"
            }
            
            let labels = []
            let data = []
            let length = placeHistory.length
            if(numDays > placeHistory.length){
                numDays = placeHistory.length
            }
            
            for(let i = numDays; i > 0; i--){
                let d = placeHistory[length-i].date
                //remove timestamp at end of date
                // labels.push(d.substring(5, d.length-13))
                labels.push(d.substring(5, d.length-13))

                //console.log(placeHistory[length-i][field])
                data.push(placeHistory[length-i][field])
            }
            if(labels.length > 20){

                labels.map(function(item, index){
                    if((index%3) == 0){                        
                    }
                    else{
                        labels[index] = ""
                    }
                })
            }

            let chart = {
                labels: labels,
                datasets: [
                    {
                        label: label,
                        data: data,
                        borderWidth: 1,
                    }
                ]
            }            
            return chart
        },
        changeData(){
            this.graphData = this.generateChartData(this.countryHistory, 'total_cases', 7)
        }
    }
}
</script>

<style scoped>

</style>