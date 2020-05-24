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
                    <country-graph class="mb-2" :options="options" v-if="casesData != null" :chart-data="casesData"/>
                    </div>
                </b-tab>
                <b-tab no-body title="Deaths">
                    <div class="text-center">
                    <b-spinner v-if="!loaded"></b-spinner>
                    <country-graph class="mb-2" :options="options" v-if="deathsData != null" :chart-data="deathsData"/>
                    </div>
                </b-tab>
                <b-tab no-body title="Tests">
                    <div class="text-center">
                    <b-spinner v-if="!loaded"></b-spinner>
                    <country-graph class="mb-2" :options="options" v-if="testsData != null" :chart-data="testsData"/>
                    </div>
                </b-tab>
            </b-tabs>
            <div class="d-flex">
            <b-dd id="dateDropdown" :text="timePeriod" class="m-md-2 flex-fill">
                <b-dropdown-item-button @click='setTime("week")'>Week</b-dropdown-item-button>
                <b-dropdown-item-button @click='setTime("month")'>Month</b-dropdown-item-button>
                <b-dropdown-item-button @click='setTime("all")'>All Data</b-dropdown-item-button>
            </b-dd>
            <b-dd id="dataDropdown" :text="cases" class="m-md-2 flex-fill">
                <b-dropdown-item-button @click='setData("New")'>New</b-dropdown-item-button>
                <b-dropdown-item-button @click='setData("Total")'>All</b-dropdown-item-button>
            </b-dd>
            </div>
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
                        ticks: {
                            callback: (value) => {
                                return this.numberWithCommas(value)
                            }
                        }
                    }]
                },

            },
            timePeriod: "Month",
            cases: "Total",
            countryHistory: [],
            loaded: false,
            casesData: null,
            deathsData: null,
            testsData: null,
            currDays: 30
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
    created(){        let baseUrl = "https://keane.pythonanywhere.com/owid/history/"
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
        numberWithCommas(val) {
            return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        },
        setTime(time){
            let num = this.countryHistory.length
            let type = "total"
            if(this.cases == "Total"){
                type = "total"
            }
            else {
                type = "new"
            }
            switch(time){
                
                case "week":
                    
                    this.casesData = this.generateChartData(this.countryHistory, type.concat('_cases'), 7)
                    this.deathsData = this.generateChartData(this.countryHistory, type.concat('_deaths'), 7)
                    this.testsData = this.generateChartData(this.countryHistory, type.concat('_tests'), 7)
                    this.timePeriod = "Week"
                    break;
                case "month":
                    this.casesData = this.generateChartData(this.countryHistory, type.concat('_cases'), 30)
                    this.deathsData = this.generateChartData(this.countryHistory, type.concat('_deaths'), 30)
                    this.testsData = this.generateChartData(this.countryHistory, type.concat('_tests'), 30)
                    this.timePeriod = "Month"
                    break;
                case "all":
                    
                    this.casesData = this.generateChartData(this.countryHistory, type.concat('_cases'), num)
                    this.deathsData = this.generateChartData(this.countryHistory, type.concat('_deaths'), num)
                    this.testsData = this.generateChartData(this.countryHistory, type.concat('_tests'), num)
                    this.timePeriod = "All"
                    break;
                default:
                    break;
            }
        },
        setData(data){
            let num = this.countryHistory.length
            let number = 0
            switch(this.timePeriod){
                    case "Week":
                        number = 7
                        break;
                    case "Month":
                        number = 30
                        break;
                    case "All":
                        number = num
                        break;
                    default:
                        number = 30
                }
            switch(data){    
                case "Total":
                    this.casesData = this.generateChartData(this.countryHistory, 'total_cases', number)
                    this.deathsData = this.generateChartData(this.countryHistory, 'total_deaths', number)
                    this.testsData = this.generateChartData(this.countryHistory, 'total_tests', number)
                    this.cases = "Total"
                    break;
                case "New":
                    this.casesData = this.generateChartData(this.countryHistory, 'new_cases', number)
                    this.deathsData = this.generateChartData(this.countryHistory, 'new_deaths', number)
                    this.testsData = this.generateChartData(this.countryHistory, 'new_tests', number)
                    this.cases = "New"
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

                //extrapolate past test data if zero
                if(field == 'total_tests'){
                    let tests = placeHistory[length-i][field]
                    if(tests == 0){
                        let j = 1
                        let toPush = 0
                        while(j < (length-i)){
                            if(placeHistory[length-i-j].total_tests != 0){
                                toPush = placeHistory[length-i-j].total_tests
                                break;
                            }
                            else{
                                j++
                                continue
                            }
                        }
                        data.push(toPush)
                    }else{
                        data.push(tests)
                    }
                }
                else{
                    data.push(placeHistory[length-i][field])
                }
            }
            
            if(labels.length > 20){

                labels.map(function(item, index){
                    if((index%3) != 0){  
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