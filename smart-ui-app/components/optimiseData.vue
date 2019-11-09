<template>
  <v-flex xs12 sm6 offset-sm3>
    <v-card>
      <v-card-title primary-title>
        <div>
          <h3 class="headline mb-0">Optimisation Result</h3>
          <div>
            <p>{{ result }}</p>
          </div>
        </div>
      </v-card-title>
    </v-card>
  </v-flex>
</template>
<script>
import axios from "axios";
export default {
  data() {
    return {
      result: null,
      users: [],
      schedules: [],
      totalProfit: null,
      battery_status: null,
      battery_energy: null
    };
  },
  mounted() {
    this.loadDemand();
  },
  methods: {
    async loadDemand() {
      /*let data =
        '{"data":[{"users[0]":{"schedule":[],"bill":0}},{"users[1]":{"schedule":[],"bill":0}}],"profit": 0, "battery_status":[],"battery_energy":[]}';*/
        let {data} = await axios.get(`http://localhost:4070/optimize`);
      //await axios.get(`http://0.0.0.0:5050/building/`+this.selectedBuildingId);
      /* let jsonData = JSON.parse(data);
      for (var k in jsonData) {
        var gData = jsonData[k];
        if (k == "data") {
          for (var i in gData){
              this.users.push({'Name':gData[i]});

          }
          console.log("1",this.users[0].Name.users[0]);
          // console.log(jsonData[k]);
        }
        if(k=="profit") {
            console.log(k);
            console.log(jsonData[k]);
        }
        if(k=="battery_status") {
            console.log(k);
            console.log(jsonData[k]);
        }
        if(k=="battery_energy") {
            console.log(k);
            console.log(jsonData[k]);
        }
      }
      // console.log(JSON.parse(data)["data"][0]["users[0]"]); */
      this.result = data;
    }
  }
};
</script>
