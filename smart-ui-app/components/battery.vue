<template>
  <v-layout>
    <v-flex xs12 sm6 offset-sm3>
      <v-card>
        <v-card-title primary-title>
          <div>
            <h3 class="headline mb-0">Battery Data and Status</h3>
            <div>
              <h4>Efficiency : {{ efficiency }}</h4>
            </div>
            <div>
              <h4>Time Interval: {{timeInterval}}</h4>
            </div>
            <div>
              <h4>Initial Energy: {{initialEnergy}}</h4>
            </div>
            <div>
              <h4>Self Discharge Rate : {{ selfDischargeRate }}</h4>
            </div>
            <div>
              <h4>Power Level : {{powerLevel}}</h4>
            </div>
            <div>
              <h4>Maximum charge capacity: {{chargeSpecs}}</h4>
            </div>
            <div>
              <h4>Maximum discharge capacity: {{dischargeSpecs}}</h4>
            </div>
            <div>
              <h4>Maximum Energy capacity: {{energySpecs}}</h4>
            </div>
          </div>
          <v-progress-circular
            :rotate="-90"
            :size="energySpecs"
            :width="110"
            :value="powerLevel"
            color="primary"
          >
            <div>
              <h4 align-center>Power Level: {{ powerLevel }}</h4>
            </div>
            <div>
              <h4 align-center>Current State : {{ chargingState }}</h4>
            </div>
          </v-progress-circular>
        </v-card-title>
      </v-card>
    </v-flex>
  </v-layout>
</template>
<script>
import axios from "axios";
export default {
  data() {
    return {
      status: "",
      efficiency: "",
      chargingState: "",
      timeInterval: "",
      initialEnergy: "",
      selfDischargeRate: "",
      powerLevel: "",
      chargeSpecs: "",
      dischargeSpecs: "",
      energySpecs: ""
    };
  },
  mounted() {
    this.getBatteryData();
  },
  methods: {
    async getBatteryData() {
      let { data } = await axios.get(`http://0.0.0.0:4000/getBatteryData`);
      for (let index = 0; index < data.length; index++) {
        console.log(data[index]["efficiency"]);
        this.status = data[index]["status"];
        this.efficiency = data[index]["efficiency"];
        this.timeInterval = data[index]["time_interval"];
        this.chargingState = data[index]["charging_state"];
        this.initialEnergy = data[index]["initial_energy"];
        this.selfDischargeRate = data[index]["self_discharge_rate"];
        this.powerLevel = data[index]["power_level"];
        this.chargeSpecs = data[index]["charge_specs"];
        this.dischargeSpecs = data[index]["discharge_specs"];
        this.energySpecs = data[index]["energy_specs"];
      }
    }
  }
};
</script>
