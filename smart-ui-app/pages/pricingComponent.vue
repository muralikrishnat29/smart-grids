<template>
  <v-container>
      <v-alert
      :value="true"
      type="info"
      v-if="selectedType.Id==1"
    >
      Change the type of pricing information to view
    </v-alert>
    <v-flex xs12>
      <v-flex xs6>
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
      <div v-if="selectedType.Id==1">
        <v-flex xs12 sm6 md12 align-center>
          <v-text-field
            readonly
            solo
            value="Today's Pricing Trend in Euros per MW"
          ></v-text-field>
        </v-flex>  
        <line-chart :key="todayKey" :chartData="currentDaydatacollection" :options="options"></line-chart>
      </div>
      <div v-if="selectedType.Id==2">
        <v-flex xs12 sm6 md12 align-center>
          <v-text-field
            readonly
            solo
            value="Tomorrow's Pricing Trend in Euros per MW"
          ></v-text-field>  
        </v-flex>
        <line-chart :key="tomorrowKey" :chartData="tomorrowdatacollection" :options="options"></line-chart>
      </div>
      <div v-if="selectedType.Id==3">
          <v-flex xs12 sm6 md12 align-content-center>
          <v-text-field
            readonly
            align-center
            solo
            value="Pricing Trend for the next 24 Hours in Euros per MW"
          ></v-text-field>
        </v-flex>
        <line-chart :key="forecastKey" :chartData="forecastdatacollection" :options="options"></line-chart>
      </div>
      <v-flex>
      <v-card class="mx-auto" color="#227093" dark max-width="400">
        <v-card-title>
          <span class="title font-weight-light">Current Price per kW</span>
        </v-card-title>
        <v-card-text
          class="headline font-weight-bold"
        >{{currentPrice/1000}}</v-card-text>
      </v-card>
      </v-flex>
    </v-flex>
  </v-container>
</template>

<script>
import axios from "axios";
import LineChart from "../charts/lineChart";

export default {
  components: {
    LineChart
  },
  methods: {
    beforeDestroy () {
    clearInterval(this.polling);
    clearInterval(this.timer);
  },
    async created() {
      const config = {
        headers: {
          Accept: "application/json"
        }
      };
    },
    async updateEveryHour() {
      this.todayKey+=1;
      this.tomorrowKey+=1;
      this.forecastKey+=1;
      console.log("s",this.todayKey);
    },
    async fillData() {
      if(this.selectedType.Id==1) {
          this.todayPricing = await this.getCurrentDayData();
      }
      else if(this.selectedType.Id==2) {
          this.tomorrowPricing = await this.getTomorrowData();
      }
      else if(this.selectedType.Id==3) {
          this.forecastPricing = await this.getForecast();
      }
      this.currentPrice = await this.getCurrentPrice();
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
        steppedLine: true,
        spanGaps: true,
        elements: {
          line: {
            spanGaps: true,
            tension: 0
          }
        },
        scales: {
          xAxes: [
            {
              label: "Hour",
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
      this.currentDaydatacollection = {
        labels: hours,
        datasets: [
          {
            label: "Price in Euros",
            backgroundColor: "#3c6382",
            data: this.todayPricing
          }
        ]
      };
      this.tomorrowdatacollection = {
        labels: hours,
        datasets: [
          {
            label: "Price in Euros",
            backgroundColor: "#b71540",
            data: this.tomorrowPricing
          }
        ]
      };
      this.forecastdatacollection = {
        labels: hours,
        datasets: [
          {
            label: "Price in Euros",
            backgroundColor: "#006266",
            data: this.forecastPricing
          }
        ]
      };
    },
    async getCurrentDayData() {
      let { data } = await axios.get(`http://0.0.0.0:4050/today`);
      return data;
    },
    async getTomorrowData() {
      let { data } = await axios.get(`http://0.0.0.0:4050/tomorrow`);
      return data;
    },
    async getForecast() {
      let { data } = await axios.get(`http://0.0.0.0:4050/forecast`);
      return data;
    },
    async getCurrentPrice() {
      let { data } = await axios.get(`http://0.0.0.0:4050/current`);
      return Math.round(parseInt(data, 10));
    },
    async testFunction () {
      this.polling = setInterval(() => {
			this.fillData()
      }, 3600000);
      this.timer = setInterval(() => {
        this.updateEveryHour()
      },3600000);
    },
    async onchange(event) {
      this.selectedId = this.selectedType.Id;
      this.fillData();
      if (this.selectedId == 1) {
        this.todayKey += 1;
      } else if (this.selectedId == 2) {
        this.tomorrowKey += 1;
      } else if (this.selectedId == 3) {
        this.forecastKey += 1;
      }
    }
  },
  mounted() {
    this.fillData();
  },
  data() {
    return {
      timer: '',
      polling: null,
      currentDaydatacollection: null,
      tomorrowdatacollection: null,
      forecastdatacollection: null,
      currentPrice: null,
      todayPricing:null,
      tomorrowPricing:null,
      forecastPricing:null,
      options: null,
      selectedType: { Id: 1, Value: "Today" },
      selectedId: 0,
      todayKey: 0,
      tomorrowKey: 0,
      forecastKey: 0,
      types: [
        { Id: 1, Value: "Today" },
        { Id: 2, Value: "Tomorrow" },
        { Id: 3, Value: "Forecast" }
      ]
    };
  }
};
</script>
