<template>
  <v-layout justify-center align-center>
    <v-flex xs12 sm8 md6>
      <div>
        <bar-chart :chartData="currentdatacollection" :options="options"></bar-chart>
      </div>
    </v-flex>
    <v-flex xs12 sm8 md6>
      <div>
        <bar-chart :chartData="forecastdatacollection" :options="options"></bar-chart>
      </div>
    </v-flex>
    <v-flex xs12 sm8 md6>
      <div>
        <bar-chart :chartData="historicaldatacollection" :options="options"></bar-chart>
      </div>
    </v-flex>
  </v-layout>
</template>

<script>
import Logo from "~/components/Logo.vue";
import VuetifyLogo from "~/components/VuetifyLogo.vue";
import axios from "axios";
import BarChart from "../charts/barChart";

export default {
  components: {
    Logo,
    VuetifyLogo,
    BarChart
  },

  /*async asyncData({params}) {
    let currentWindEnergy =0;
    try {
      currentWindEnergy = await $axios.$get(`http://0.0.0.0:5050/windcurrentenergy`);
      return { currentWindEnergy };
    } catch (e) {
      return { currentWindEnergy };
    }
  },*/
  methods: {
    async created(){
      const config = {
        headers: {
          'Accept':'application/json'
        }
      }
      try {
        const res = await axios.get('https://icanhazdadjoke.com/search', config);
        console.log(res);
      } catch (error) {
        console.log(error);
      }
    },
    async fillData() {
      const windEnergy = Math.round(await this.getWindCurrentEnergy());
      const solarEnergy = Math.round(await this.getSolarCurrentEnergy());
      const windForecast = await this.getWindForecastEnergy();
      const solarForecast = await this.getPVForecastEnergy();
      const historicalForecast = await this.getForecastData();
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
      let historyHours = [];
      let historyWind  =[];
      let historySolar =[];
      for (let index = 0; index < historicalForecast.length; index++) {
        const hour = historicalForecast[index]["Hour"];
        const windEnergy = historicalForecast[index]["WindEnergy"];
        const solarEnergy = historicalForecast[index]["SolarEnergy"];
        historyHours.push(hour);
        historyWind.push(windEnergy);
        historySolar.push(solarEnergy);
      }
      console.log(historyHours,historyWind,historySolar);
      this.options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          xAxes: [
            {
              stacked: true,
              categoryPercentage: 0.5,
              barPercentage: 1,
              gridLines: {
                display: false
              }
            }
          ],
          yAxes: [
            {
              stacked: true,
              gridLines: {
                display: false
              }
            }
          ]
        }
      };
      this.currentdatacollection = {
        labels: ["Total Energy Generation Information"],
        datasets: [
          {
            label: "Wind Energy",
            backgroundColor: "#3498db",
            data: [windEnergy]
          },
          {
            label: "Solar Energy",
            backgroundColor: "#f1c40f",
            data: [solarEnergy]
          }
        ]
      };
      this.forecastdatacollection = {
        labels: hours,
        datasets: [
          {
            label: "Wind Energy",
            backgroundColor: "#3498db",
            data: windForecast
          },
          {
            label: "Solar Energy",
            backgroundColor: "#f1c40f",
            data: solarForecast
          }
        ]
      };
      console.log(historyWind);
      console.log(historySolar);
      this.historicaldatacollection = {
        labels: historyHours,
        datasets: [
          {
            label: "Wind Energy",
            backgroundColor: "#3498db",
            data: historyWind
          },
          {
            label: "Solar Energy",
            backgroundColor: "#f1c40f",
            data: historySolar
          }
        ]
      };
    },
    async getWindCurrentEnergy() {
      let { data } = await axios.get(`http://0.0.0.0:4000/windcurrentenergy`);
      return Math.round(parseInt(data, 10));
    },
    async getSolarCurrentEnergy() {
      let { data } = await axios.get(`http://0.0.0.0:4000/pvcurrentenergy`);
      return Math.round(parseInt(data, 10));
    },
    async getWindForecastEnergy() {
      let { data } = await axios.get(`http://0.0.0.0:4000/windforecastenergy`);
      return data;
    },
    async getPVForecastEnergy() {
      let { data } = await axios.get(`http://0.0.0.0:4000/pvforecastenergy`);
      return data;
    },
     async getForecastData() {
      let { data } = await axios.get(`http://0.0.0.0:4000/history`);
      return data;
    }
  },
  mounted() {
    this.fillData();
  },
  data() {
    return {
      currentdatacollection: null,
      forecastdatacollection: null,
      historicaldatacollection: null,
      currentWindEnergy: 0,
      options: null
    };
  }
};
</script>
