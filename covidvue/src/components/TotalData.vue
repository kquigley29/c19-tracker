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
        <!-- <div  style="width: 100%;" class="d-flex justify-content-between">
            <b-card class="flex-fill text-center">
                <h6><strong>Cases</strong></h6>
                <p>{{summary.total_cases}}</p>
            </b-card>
            <b-card class="flex-fill text-center">
                <h6><strong>Deaths</strong></h6>
                <p>{{summary.deaths}}</p>
            </b-card>
            <b-card class="flex-fill text-center">
                <h6><strong>Recovered</strong></h6>
                <p>{{summary.recovered}}</p>
            </b-card>

        </div> -->
        <b-row>
            <b-card class="flex-fill text-center">
                <h5><strong>Cases</strong></h5>
                <p>{{numberWithCommas(summary.total_cases)}}</p>
            </b-card>
        </b-row>
        <b-row>
            <b-card class="flex-fill text-center">
                <h5><strong>Deaths</strong></h5>
                <p>{{numberWithCommas(summary.deaths)}}</p>
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
export default {
    name: "TotalData",
    props:{
        summary: {},
        loading: Boolean,
        countries: Array
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
    computed:{
     
    }
}
</script>

<style>

</style>