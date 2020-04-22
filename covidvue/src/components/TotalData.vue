<template>
<div>
    <b-card
    header="Totals"
    >
    <p>Total Confirmed: {{summary.total_cases}}</p>
    <p>Total Deaths: {{summary.deaths}}</p>
    <p>Total Recovered: {{summary.recovered}}</p>
    </b-card>
</div>
</template>

<script>
export default {
    name: "TotalData",
    props:{
        summary: {},
        countries: Array
    },
    methods:{
        totalProp(prop){
            return this.countries.reduce(function(a,b){
                return a + b[prop];
            }, 0);
        }
    },
    computed:{
     
    }
}
</script>

<style>

</style>