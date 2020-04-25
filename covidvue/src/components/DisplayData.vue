<template>
    <div>
        <b-card class="mb-5" no-body>
        <b-tabs card>
            <b-tab no-body title="Statistics">
            <input  v-model="query" placeholder=" Country" class=" w-100 mt-3">
            <b-table 
            responsive 
            outlined 
            :filter="query"
            v-bind:current-page="currentPage" 
            v-bind:per-page="perPage" 
            :busy="isBusy"         
            striped hover 
            :items="countries" 
            :fields="fields"
            :sort-by.sync="sortBy"
            :sort-desc.sync="sortDesc"
            @row-clicked='rowClicked'>
                <template v-slot:table-busy>
                    <div class="text-center  my-2">
                    <b-spinner class="align-middle"></b-spinner>
                    <strong> Loading...</strong>
                    </div>
                </template>
                <b-pagination
                v-model="currentPage"
                :total-rows="numberRows"
                :per-page="perPage"
                ></b-pagination>
            </b-table>
            <b-pagination
                align="center"
                v-model="currentPage"
                :total-rows="numberRows"
                :per-page="perPage"
                ></b-pagination>
            </b-tab>
            <b-tab no-body :disabled="isBusy" title="Map">
                <!-- <b-card no-body> -->
                    <b-tabs @activate-tab="changeMapData" card>
                        <div class="mt-2">
                            <b-tab class="text-center" no-body title="Cases">
                                <!-- <h5>Cases per Million</h5> -->
                            </b-tab>
                            <b-tab no-body class="text-center" title="Deaths"> 
                                <!-- <h5>Deaths per Million</h5>              -->
                            </b-tab>
                            <b-tab no-body class="text-center" title="Tests">
                                <!-- <h5>Tests per Thousand</h5>          -->
                            </b-tab>
                        </div>
                    </b-tabs>
                    <MapChart lowColor="#f9fdff" highColor="#12a0e8" v-if="countries.length > 5" :countryData="mapData"/>

                <!-- </b-card> -->
            </b-tab>
        </b-tabs>
        </b-card>

        <b-modal body-class="p-1" modal-class="lg" ok-only size="lg" id="modal-1" scrollable :title=modalCountry.name>
            <country-data v-if="modalCountry != {}" :country="modalCountry"/>
            <template v-slot:modal-footer>
                <p></p>
            </template>
        </b-modal>
    </div>
</template>

<script>

//display the coountrydata component in the modal when country clicked on
import CountryData from "./CountryData.vue"
import MapChart from 'vue-map-chart'
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
    components:{
        CountryData,
        MapChart
    },
    name: "DataDisplay",
    props: {
        countries: Array,
        //isBusy prop is bound so component knows when data is received, this could be done as a data variable
        //and a method to change it in parent component which would be better
        isBusy: Boolean,
        summary: Object
    },
    watch: {
        countries: function(){
            this.changeMapData(0)
        }
        
    },

    data() {
        return{
            //default sorting
            mapData: {},
            sortBy: "total_cases",
            //sort descending
            sortDesc: true,
            //query is to search the table and is bound to the table
            query: '',
            //number of countries per page on table
            perPage: 20,
            //populated when a country is clicked on
            modalCountry: {},
            //current page  of table
            currentPage: 1,
            //fields to be used in table, the tests and per million columns are hidden for screens < medium
            fields: [
                {key: 'name', sortable: true, class: "text-center"}, 
                {key: 'total_cases', sortable: true, class:"text-center", formatter: this.numberWithCommas}, 
                {key: 'total_deaths', sortable: true, class: "text-center", formatter: this.numberWithCommas}, 
                {key: 'total_tests', sortable: true, class: "text-center d-none d-md-table-cell", formatter: this.numberWithCommasTests},
                {key: 'total_deaths_per_million', sortable: true, class: "column-class d-none d-md-table-cell text-center", formatter: this.numberWithCommas},
                {key: 'total_cases_per_million', sortable: true, class: "column-class text-center d-none d-md-table-cell", formatter: this.numberWithCommas}
                ]
        }
    },
    computed: {
        
        casesMapData: function(){
            let data = {}
            for(let i = 0; i < this.countries.length; i++){
                console.log(this.countries[[i].iso])
                data[getCode(this.countries[i].name)] = parseInt(this.countries[i].total_cases_per_million)
            }
            console.log(data)
            return data;
        },
    
        numberRows: function(){
            return this.countries.length
        },
        maxDeaths: function(){
            return Math.max.apply(Math, this.countries.map(function(o) { return o.total_deaths; }))
        },
        maxDeathsMillion: function(){
            return Math.max.apply(Math, this.countries.map(function(o) { return o.total_deaths_per_million; }))
        },
        maxCasesMillion: function(){
            return Math.max.apply(Math, this.countries.map(function(o) { return o.total_cases_per_million; }))
        },
        maxTestsThousand: function(){
            return Math.max.apply(Math, this.countries.map(function(o) { return o.total_tests_per_thousand; }))
        },
    },
    methods:{
        // formatNumber(val){
        //     return
        // },
        changeMapData(index){
            let data = {}
            for(let i = 0; i < this.countries.length; i++){
                if(index == 0){
                    data[getCode(this.countries[i].name)] = parseInt(this.countries[i].total_cases_per_million)
                }
                else if(index == 1){
                     data[getCode(this.countries[i].name)] = parseInt(this.countries[i].total_deaths_per_million)
                }
                else if(index == 2){
                     data[getCode(this.countries[i].name)] = parseInt(this.countries[i].total_tests_per_thousand)
                }
            }
            this.mapData = data;
        },
        //add commas into a number string, utility function
        numberWithCommas(val) {
            return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        },
        numberWithCommasTests(val) {
            if(val==0){
                return "-"
            }
            else return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        },
        //converts a digit to hex
        componentToHex(c) {
            var hex = c.toString(16);
            return hex.length == 1 ? "0" + hex : hex;
        },
        //converts an rgb to hex
        rgbToHex(r, g, b) {
            return "#" + this.componentToHex(r) + this.componentToHex(g) + this.componentToHex(b);
        },
        //runs when a row is clicked
        rowClicked(item, index, e){
            e.preventDefault()
            this.modalCountry = item
            this.$bvModal.show("modal-1")
            
        }
    }
}


// //this is to populate the map with data when the countries is filled from api, this is better to do 
        // //in a method call from parents but still works
        // countries: function(newVal){
        //     var vm = this;
        //     var casesMap = this.$refs.casesMap
            
        //     var casesDoc;
        //     casesMap.addEventListener("load", function(){
        //         casesDoc = casesMap.contentDocument;
                
        //         for(let i=0; i<newVal.length; i++){
        //             var r = '[data-name="';
        //             var s = r.concat(newVal[i].name)
        //             var t = s.concat('"]')
        //             try{
                        
        //                 var path = casesDoc.querySelectorAll(t)
        //                 var val = Math.round(255 - ((newVal[i].total_cases_per_million / vm.maxCasesMillion) * 255))
        //                 path[0].style.fill=vm.rgbToHex(val, val, val)
                        
        //             }
        //             catch(e){
        //                 console.log(e)
        //             }
        //         }
        //     })
        //     var deathsMap = this.$refs.deathsMap
        //     var deathsDoc;
        //     deathsMap.addEventListener("load", function(){
        //         deathsDoc = deathsMap.contentDocument;
        //         for(let i=0; i<newVal.length; i++){
        //             var r = '[data-name="';
        //             var s = r.concat(newVal[i].name)
        //             var t = s.concat('"]')
        //             try{
        //                 var path = deathsDoc.querySelectorAll(t)
        //                 var val = Math.round(255 - ((newVal[i].total_deaths_per_million / vm.maxDeathsMillion) * 255))
        //                 path[0].style.fill=vm.rgbToHex(val, val, val)
                        
        //             }
        //             catch(e){
        //                 console.log(e)
        //             }
        //         }
        //     })
        //     var testsMap = this.$refs.testsMap
        //     var testsDoc;
        //     testsMap.addEventListener("load", function(){
        //         testsDoc = testsMap.contentDocument;
        //         for(let i=0; i<newVal.length; i++){
        //             var r = '[data-name="';
        //             var s = r.concat(newVal[i].name)
        //             var t = s.concat('"]')
        //             try{
        //                 var path = testsDoc.querySelectorAll(t)
        //                 var val = Math.round(255 - ((newVal[i].total_tests_per_thousand / vm.maxTestsThousand) * 255))
        //                 path[0].style.fill=vm.rgbToHex(val, val, val)
                        
        //             }
        //             catch(e){
        //                 console.log(e)
        //             }
        //         }
        //     })
        // }
</script>

<style>
    .column-class{
        
        max-width: 130px;
    }
</style>