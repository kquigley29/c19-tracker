<template>
<div style= "height: 100%" class="text-center">
    <b-card
    header="World Totals"
    no-body
    style="height: 100%"
    >
    <b-container style="height: 100%;">
    <b-row v-if="loading" style="height: 100%">
        <b-col>
            <div>
                <b-spinner class="align-middle"></b-spinner>
                <strong> Loading...</strong>
            </div>
        </b-col>
    </b-row>

    <div style="height: 100% " v-else>
        <b-row>
            <b-card class="flex-fill text-center">
                <h5><strong>Cases</strong></h5>
                <p>{{numberWithCommas(summary.total_cases)}}</p>
                <p>{{casesChange}}% change from last week</p>
            </b-card>
        </b-row>
        <b-row>
            <b-card class="flex-fill text-center">
                <h5><strong>Deaths</strong></h5>
                <p>{{numberWithCommas(summary.deaths)}}</p>
                <p>{{deathsChange}}% change from last week</p>
            </b-card>
        </b-row>
        <b-row class="flex-grow" style="">
            <b-card style="border-bottom: 0px" class="flex-fill text-center">
                <h5><strong>Recovered</strong></h5>
                <p>{{numberWithCommas(summary.recovered)}}</p>
                
            </b-card>
        </b-row>
    </div>

    </b-container>
    </b-card>
</div>
</template>

<script>
import axios from 'axios';

export default {


    name: "TotalData",
    props:{
        summary: {},
        loading: Boolean,
        countries: Array
    },
    data(){
        return {
            worldData: []
        }
    },
    computed:{
        casesChange: function(){
        
            let thisWeek=this.worldData.slice((this.worldData.length-8), (this.worldData.length-1))           
            let lastWeek=this.worldData.slice((this.worldData.length-15), (this.worldData.length-8))
            console.log(thisWeek.reduce(function(a,b){
                return a + b['new_cases'];
                }, 0));
            let thisSum = thisWeek.reduce(function(a,b){
                return a + b['new_cases'];
                }, 0);
            let lastSum = lastWeek.reduce(function(a,b){
                return a + b['new_cases'];
                }, 0)
            return (((thisSum-lastSum)/((thisSum+lastSum)/2))*100).toFixed(2)
        },
        deathsChange: function(){
        
            let thisWeek=this.worldData.slice((this.worldData.length-8), (this.worldData.length-1))           
            let lastWeek=this.worldData.slice((this.worldData.length-15), (this.worldData.length-8))
            let thisSum = thisWeek.reduce(function(a,b){
                return a + b['new_deaths'];
                }, 0);
            let lastSum = lastWeek.reduce(function(a,b){
                return a + b['new_deaths'];
                }, 0)
            return (((thisSum-lastSum)/((thisSum+lastSum)/2))*100).toFixed(2)
        }
    },
    methods:{
        totalProp(prop){
            return this.countries.reduce(function(a,b){
                return a + b[prop];
            }, 0);
        },
        numberWithCommas(val) {
            return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        },
    },

    mounted(){
        axios.get("https://keane.pythonanywhere.com/owid/history/World")
        .then(res => {
            this.worldData = res.data
            console.log(this.worldData)
        })
    }

}
</script>

<style>

</style>