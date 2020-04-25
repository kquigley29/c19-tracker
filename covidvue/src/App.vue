<template>
  <div id="app">
    <b-container fluid="md">
    <b-row class="mb-2" align-v="center">
      <b-col class="text-center">
        
      <!-- <a target="_blank" href="https://www.visceraltd.com/"><b-img class="mb-5" fluid :src="require('./assets/VisceraLogo.png')"/></a> -->
        <a target="_blank" href="https://www.visceraltd.com/"><img class="mb-5" style="width: 80%" fluid src='./assets/VisceraLogo.png'/></a>
      </b-col>
      <b-col>
        <world-data :countryData="{US: 500,
        GB: 300
        }"/>
      </b-col>
    </b-row>
    <b-row>
      <b-col md>
        <total-data :loading="summaryLoading" class="mb-2" style="width:" v-bind:summary="casesSummary" v-bind:countries="countryList"/>
      </b-col>
      <b-col md>
        <total-data :loading="summaryLoading" class="mb-2" style="width:" v-bind:summary="casesSummary" v-bind:countries="countryList"/>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
      <display-data id="display" ref="displayData" v-bind:summary="casesSummary" v-bind:isBusy="isBusy" class="" v-bind:countries='countryList'/>
      </b-col>
    </b-row>
    </b-container>
  </div>
</template>

<script>

import DisplayData from './components/DisplayData.vue'
import TotalData from './components/TotalData.vue'
import WorldChange from './components/WorldChange.vue'
import WorldData from './components/Map/WorldData.vue'
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return{
      countryList: [],
      casesSummary: {},
      isBusy: true,
      summaryLoading: true
    }
  },
  components: {
    DisplayData,
    TotalData,
    WorldChange,
    WorldData
  },
  methods:{

  },
  mounted(){
    //get the country data from our api
    axios.get("https://keane.pythonanywhere.com/all")
      .then(res => {
        //console.log(display);
        this.countryList = res.data;
        //console.log(this.countryList)
        this.isBusy = false;
      })
      
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
