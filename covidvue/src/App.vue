<template>
  <div id="app">
    <b-container fluid="md">
    <b-row class="mb-2" align-v="center">
      <b-col md class="text-center">
          <a target="_blank" href="https://www.visceraltd.com/"><img class="mb-5" style="width: 30%" fluid src='./assets/VisceraLogo.png'/></a>
      </b-col>
      
    </b-row>
    <!-- <b-container> -->
    <b-row class="mb-2" style="height: 100%;">
     
      <b-col class= "align-items-center" md stylel="height: 100%">
        <div></div>
        <total-data :loading="summaryLoading" style="height: 100%" class="align-self-stretch flex-fill" v-bind:summary="casesSummary" v-bind:countries="countryList"/>
       
      </b-col>
      <b-col class="text-center" md>
        <b-card style="height: 100%" header="World Weekly Change">
        <b-container>
        <b-row>
        <world-change style="width: 100%" v-bind:countries="countryListLong"/>
        </b-row>
        <b-row class="mt-2">
          <b-col md>
            <div class="d-flex align-items-center">
              <b-card style="background: #860000; max-height: 15px; max-width: 15px" class="mr-3">
                
              </b-card>
              <p>Cases this week > Cases last week</p>
              <p>

              </p>
            </div>
          </b-col>
          <b-col md>
            <div class="d-flex align-items-center">
              <b-card style="background: #548235; max-height: 15px; max-width: 15px" class="mr-3">
                
              </b-card>
              <p>Cases this week &lt; Cases last week</p>
              <p>

              </p>
            </div>
          </b-col>
        </b-row>
        </b-container>
        </b-card>

      </b-col>
      
      <!-- <b-col md>
        <total-data :loading="summaryLoading" class="mb-2" style="width:" v-bind:summary="casesSummary" v-bind:countries="countryList"/>
      </b-col> -->
    </b-row>
    <!-- </b-container> -->
    <b-row>
      <b-col>
      <display-data :countryStringency="countryStringency" id="display" ref="displayData" v-bind:summary="casesSummary" v-bind:isBusy="isBusy" class="" v-bind:countries='countryList'/>
      </b-col>
    </b-row>
    </b-container>
  </div>
</template>

<script>

import DisplayData from './components/DisplayData.vue'
import TotalData from './components/TotalData.vue'
import WorldChange from './components/WorldChange.vue'
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return{
      countryList: [],
      countryListLong: {},
      countryStringency: [],
      casesSummary: {},
      isBusy: true,
      summaryLoading: true
    }
  },
  components: {
    DisplayData,
    TotalData,
    WorldChange,
  },
  methods:{

  },
  mounted(){
    //get the country data from our api
    axios.get("https://keane.pythonanywhere.com/owid/current/all")
      .then(res => {
        this.countryList = res.data;
        //console.log(this.countryList)
        this.isBusy = false;
      })
      .catch(e => console.log(e))

    axios.get("https://keane.pythonanywhere.com/owid/history/allRecent")
    .then(res => {
      this.countryListLong = res.data;
    })
    .catch(e => console.log(e));

    axios.get("https://keane.pythonanywhere.com/oxford/current/all")
    .then(res => {
      this.countryStringency = res.data;
    })
    .catch(e => console.log(e));
    
      
    //get the summary data from this api
    //TODO: Add this data to the api
    axios.get("https://api.quarantine.country/api/v1/summary/latest") 
    .then(res => {
      var e = res.data
      this.casesSummary = e.data.summary
      this.summaryLoading = false
    }) 
  }
}
</script>

<style lang='scss'>

  @import './style/custom.scss';

#app {
  
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
 
  color: #2c3e50;
  margin-top: 60px;

}
</style>
