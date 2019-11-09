<template>
  <v-container fluid>
    <v-layout row wrap align-center>
      <v-flex xs6>
        <v-select
          v-model="selectedBuilding"
          :items="buildings"
          item-text="Value"
          item-value="Id"
          label="Select"
          persistent-hint
          return-object
          single-line
          @change="onchange"
        ></v-select>
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script>
import axios from "axios";
  export default {
    mounted() {
        this.getBuildingNames();
    },
    methods: {
        async getBuildingNames() {
            let { data } = await axios.get(`http://0.0.0.0:5050/buildings`);
            console.log(data);
            for (let index = 0; index < data.length; index++) {
                this.buildings.push({Id:data[index]["Id"],Value:data[index]["BuildingName"]})
            }
            console.log(this.buildings);
        },
        async onchange(event) {
            this.$emit('buildingSelected',this.selectedBuilding);
        }
    },
    data () {
      return {
        buildings:[],
        selectedBuilding:{}
      }
    }
  }
</script>

