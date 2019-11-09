<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="600px">
      <template v-slot:activator="{ on }">
        <v-btn color="#227093" dark v-on="on">Update Battery</v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="headline">Update Battery</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-text-field label="Efficiency*" v-model="form.efficiency" required></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field label="Time Interval*" v-model="form.timeInterval" required></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field label="Charge Specs*" v-model="form.chargeSpecs" required></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field label="Discharge Specs*" v-model="form.dischargeSpecs" required></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field label="Energy Specs*" v-model="form.energySpecs" required></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field label="Initial Energy*" v-model="form.initialEnergy" required></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  label="Self Discharge Rate*"
                  v-model="form.selfDischargeRate"
                  required
                ></v-text-field>
              </v-flex>
            </v-layout>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="dialog = false">Close</v-btn>
          <v-btn color="blue darken-1" flat @click="onBatterySubmit">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>
<script>
import axios from "axios";
export default {
  data: () => ({
    dialog: false,
    form: {
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
    }
  }),
  mounted() {
    this.getBatteryData();
  },
  methods: {
    async getBatteryData() {
      let { data } = await axios.get(`http://0.0.0.0:4000/getBatteryData`);
      for (let index = 0; index < data.length; index++) {
        console.log(data[index]["efficiency"]);
        this.form.status = data[index]["status"];
        this.form.efficiency = data[index]["efficiency"];
        this.form.timeInterval = data[index]["time_interval"];
        this.form.chargingState = data[index]["charging_state"];
        this.form.initialEnergy = data[index]["initial_energy"];
        this.form.selfDischargeRate = data[index]["self_discharge_rate"];
        this.form.powerLevel = data[index]["power_level"];
        this.form.chargeSpecs = data[index]["charge_specs"];
        this.form.dischargeSpecs = data[index]["discharge_specs"];
        this.form.energySpecs = data[index]["energy_specs"];
      }
    },
    async onBatterySubmit(event) {
      this.dialog = false;
      await this.updateBattery(
        this.form.status,
        this.form.efficiency,
        this.form.timeInterval,
        this.form.chargingState,
        this.form.initialEnergy,
        this.form.selfDischargeRate,
        this.form.powerLevel,
        this.form.chargeSpecs,
        this.form.dischargeSpecs,
        this.form.energySpecs
      );
      this.$emit("batteryUpdated", "batteryUpdate");
      await this.getBatteryData();
    },
    async updateBattery(
      status,
      efficiency,
      timeInterval,
      chargingState,
      initialEnergy,
      selfDischargeRate,
      powerLevel,
      chargeSpecs,
      dischargeSpecs,
      energySpecs
    ) {
      let { data } = await axios.get(
        `http://0.0.0.0:4000/updateBatteryDetails/` +
          efficiency +
          `/` +
          timeInterval +
          `/` +
          chargeSpecs +
          `/` +
          dischargeSpecs +
          `/` +
          energySpecs +
          `/` +
          initialEnergy +
          `/` +
          selfDischargeRate +
          `/`
      );
      console.log(data);
    }
  }
};
</script>