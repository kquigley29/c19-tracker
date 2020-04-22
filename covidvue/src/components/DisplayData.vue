<template>
    <div>
        <b-card class="mb-5" no-body>
        <b-tabs card>
            <b-tab title="Statistics">
            <input  v-model="query" placeholder="Country" class="mb-2 w-100 mt-3">
            <b-table 
            responsive 
            outlined 
            v-bind:current-page="currentPage" 
            v-bind:per-page="perPage" 
            :busy="isBusy"         
            striped hover 
            :items="computedList" 
            :fields="fields"
            :sort-compare="onSorted"
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
            <b-tab :disabled="isBusy" title="Map">
                <object id="worldmap" type="image/svg+xml" width="100%" height="10%" ref="map" data="assets/world.svg"></object>
            
            </b-tab>
        </b-tabs>
        </b-card>

        <b-modal id="modal-1" title="Country Data">
            <country-data v-if="modalCountry != {}" :country="modalCountry"/>
        </b-modal>
    </div>
</template>

<script>

//display the coountrydata component in the modal when country clicked on
import CountryData from "./CountryData.vue"

export default {
    components:{
        CountryData
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
        //this is to populate the map with data when the countries is filled from api, this is better to do 
        //in a method call from parents but still works
        countries: function(newVal){
            var a = document.querySelector("#worldmap");
            var vm = this;
            var svgDoc;
            console.log(newVal)
            a.addEventListener("load", function(){
                svgDoc = a.contentDocument;
                for(let i=0; i<newVal.length; i++){
                    var r = '[data-name="';
                    var s = r.concat(newVal[i].name)
                    var t = s.concat('"]')
                    try{
                        var path = svgDoc.querySelectorAll(t)
                        var val = Math.round(255 - ((newVal[i].total_deaths / vm.maxDeaths) * 255))
                        path[0].style.fill=vm.rgbToHex(val, val, val)
                        
                    }
                    catch(e){
                        console.log(e)
                    }
                }
            })
        }
    },

    data() {
        return{
            //query is to search the table and is bound to the table
            query: '',
            //number of countries per page on table
            perPage: 20,
            //populated when a country is clicked on
            modalCountry: {},
            //current page  of table
            currentPage: 1,
            //fields to be used in table
            fields: [
                {key: 'name', sortable: true}, 
                {key: 'total_cases', sortable: true}, 
                {key: 'total_deaths', sortable: true}, 
                {key: 'total_tests', sortable: true}
                ]
        }
    },
    computed: {
        //this is the computed list which is displayed in the table, this replaces the 0 with - and puts commas in
        //then filters for the search query
        computedList: function () {
            var vm = this
            let tempList = this.countries
            tempList.forEach(element => {
                element.total_cases = this.numberWithCommas(element.total_cases)
                element.total_deaths = this.numberWithCommas(element.total_deaths)
                element.total_tests = this.numberWithCommas(element.total_tests)
                
                if(element.total_tests == '0'){
                    element.total_tests = '-'
                }
            });
            return tempList.filter(function (item) {
                return item.name.toLowerCase().indexOf(vm.query.toLowerCase()) !== -1
            }) 
        },
        numberRows: function(){
            return this.computedList.length
        },
        maxDeaths: function(){
            return Math.max.apply(Math, this.countries.map(function(o) { return o.total_deaths; }))
        },
        maxDeathsMillion: function(){
            return Math.max.apply(Math, this.countries.map(function(o) { return o.total_deaths_per_million; }))
        },
    },
    methods:{
        onSorted(a, b, field){
            if(field == 'name'){
                if(a.name < b.name){
                    return -1
                }
                else if(a.name == b.name){
                    return 0
                }
                else{
                    return 1
                }
            }
            else{
                
                //replace the "," in the parsed table values
                let aVal = parseInt(a[field].replace(new RegExp(",", "g"), "").replace("-", "0"))
                let bVal = parseInt(b[field].replace(new RegExp(",", "g"), "").replace("-", "0"))
                
                if(aVal < bVal){
                    return -1
                }
                else if(aVal == bVal){
                    return 0
                }
                else{
                    return 1
                }
            }
        
        },
        //add commas into a number string, utility function
        numberWithCommas(x) {
            return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
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

</script>

<style scoped>

</style>