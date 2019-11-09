<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="600px">
      <template v-slot:activator="{ on }">
        <v-btn color="#227093" dark v-on="on">Add Device</v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="headline">Add Device</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-text-field label="Name*" v-model="form.deviceName" required></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field label="EST(h)*" v-model="form.est" required></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field label="LET(h)*" v-model="form.let" required></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field label="LOT(h)*" v-model="form.lot" required></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field label="Power(kW)*" v-model="form.power" required></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field label="Initial Start Time*" v-model="form.startTime" required></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field label="Initial Stop Time*" v-model="form.stopTime" required></v-text-field>
              </v-flex>
            </v-layout>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="dialog = false">Close</v-btn>
          <v-btn color="blue darken-1" flat @click="onDeviceSubmit">Save</v-btn>
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
        deviceName:'',
        est:'',
        let:'',
        lot:'',
        power:'',
        startTime:'',
        stopTime:''
      }
    }),
    props: ['selectedBuilding'],
    methods: {
        async onDeviceSubmit(event) {
            this.dialog=false;
            await this.submitDevice(this.form.deviceName,this.form.est,this.form.let,this.form.lot,this.form.power,this.form.startTime,this.form.stopTime);
            this.$emit('deviceSubmitted','deviceSubmit');
            this.form.deviceName=this.form.est=this.form.let=this.form.lot=this.form.power=this.form.startTime=this.form.endTime="";
        },
        async submitDevice(deviceName, est, LET, lot, power, startTime, endTime) {
            let { data } = await axios.get(`http://0.0.0.0:5050/addDevice/`+est+`/`+LET+`/`+power+`/`+lot+`/`+deviceName+`/`+startTime+`/`+endTime+`/`+this.selectedBuilding+`/`);
            console.log(data);
        }
    }
  }
</script>