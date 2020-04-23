<template>
  <div id="app">
    <b-container fluid="md">
    <b-row class="justify-content-center">
      <a target="_blank" href="https://www.visceraltd.com/"><img  class="mb-5" src="./assets/VisceraLogo.png"/></a>
    </b-row>
    <b-row>
      <b-col sm>
        <total-data class="mb-2" v-bind:summary="casesSummary" v-bind:countries="countryList"/>
      </b-col>
      
    </b-row>
    <b-row>
      <b-col>
      <display-data id="display" ref="displayData" v-bind:summary="casesSummary" v-bind:isBusy="isBusy" class="mt-3" v-bind:countries='countryList'/>
      </b-col>
    </b-row>
    </b-container>
  </div>
</template>

<script>

import DisplayData from './components/DisplayData.vue'
import TotalData from './components/TotalData.vue'
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return{
      countryList: [],
      casesSummary: {},
      isBusy: true
    }
  },
  components: {
    DisplayData,
    TotalData
  },
  methods:{

  },
  mounted(){
    //get the country data from our api
    axios.get("https://keane.pythonanywhere.com/all")
      .then(res => {
        //console.log(display);
        this.countryList = res.data;
        this.isBusy = false;
      })
      
    //get the summary data from this api
    //TODO: Add this data to the api
    axios.get("https://api.quarantine.country/api/v1/summary/latest") 
    .then(res => {
      var e = res.data
      this.casesSummary = e.data.summary
    }) 
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
 
  color: #2c3e50;
  margin-top: 60px;
}
</style>
