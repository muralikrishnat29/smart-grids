<template>
<v-container>
    <v-alert
      :value="true"
      type="info"
      v-if="selectedBuildingId==0"
    >
      Select a building to view the demand information
    </v-alert>
    <building @buildingSelected="buildingChange"></building>
    <v-flex xs6 row wrap align-center>
    <v-select
          v-model="selectedType"
          :items="types"
          item-text="Value"
          item-value="Id"
          label="Select"
          persistent-hint
          return-object
          single-line
          @change="onchange"
        ></v-select>
    </v-flex>
    <bar-chart v-if="selectedBuildingId>0" :key="buildingSelectedKey" :chartData="demandDataCollection" :options="options"></bar-chart>
    <br/>
    <v-flex xs12 v-if="selectedType.Id==2">
      <v-card>
        <v-toolbar color="primary" dark>
          <v-toolbar-title>List of controllable devices</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-list>
          <v-list-tile
            v-for="item in devices"
            :key="item"
          >
            <v-list-tile-content>
              <v-list-tile-title v-text="item"></v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-card>
    </v-flex>
</v-container>
</template>
<script>
import building from "~/components/buildingList.vue";
import axios from "axios";
import BarChart from "../charts/barChart";
export default {
  components: {
    building,
    BarChart
  },
  data() {
    return {
      buildingSelectedKey: 0,
      selectedBuildingId: 0,
      selectedType: { Id: 1, Value: "Total Demand" },
      selectedId: 1,
      devices: null,
      demandDataCollection: null,
      options: null,
      types: [
        { Id: 1, Value: "Total Demand" },
        { Id: 2, Value: "Controllable Devices Demand" }
      ]
    };
  },
  methods: {
    async fillData() {
        const buildingData = await this.loadDemand();
        let buildingDemand;
        if(this.selectedType.Id==1){
            buildingDemand = buildingData[0] ["TotalDemand"];
        }
        else if(this.selectedType.Id==2){
            buildingDemand = buildingData[0] ["CEDConsumption"];
            const deviceList = buildingData[0]["CED_List"].replace(/'/g, '"');
            this.devices = JSON.parse(deviceList);
        }
        const hours = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24
      ];
        this.options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          xAxes: [
            {
              categoryPercentage: 0.5,
              barPercentage: 1,
              gridLines: {
                display: false
              }
            }
          ],
          yAxes: [
            {
              gridLines: {
                display: false
              }
            }
          ]
        }
      };
      this.demandDataCollection = {
        labels: hours,
        datasets: [
          {
            label: "Demand in KW",
            backgroundColor: "#40739e",
            data: JSON.parse(buildingDemand)
          }
        ]
      };
    },
    async buildingChange(value) {
      this.selectedBuildingId = value.Id;
      this.fillData();
      this.buildingSelectedKey += 1;
    },
    async onchange(event) {
      this.selectedId = this.selectedType.Id;
      this.fillData();
      this.buildingSelectedKey+=1;
    },
    async loadDemand(){
        let { data } = await axios.get(`http://0.0.0.0:5050/building/`+this.selectedBuildingId);
        return data;
    }
  }
};
</script>
