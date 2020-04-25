<template>
<div class="text-center">
    <b-card
    header="World Totals"
    no-body
    >
    <b-container>
    <b-row>
        <b-col v-if="loading">
            <div>
                <b-spinner class="align-middle"></b-spinner>
                <strong> Loading...</strong>
            </div>
        </b-col>
        <div v-else style="width: 100%;" class="d-flex justify-content-between">
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

        </div>
    </b-row>
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
        }
    },
    computed:{
     
    }
}
</script>

<style>

</style>