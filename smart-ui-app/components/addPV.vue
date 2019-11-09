<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="600px">
      <template v-slot:activator="{ on }">
        <v-btn color="#227093" dark v-on="on">Add Solar Panel</v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="headline">Add Solar Panel</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-text-field label="Area*" v-model="form.area" required></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field label="Maximum Energy*" v-model="form.emax" required></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field label="Angle of module*" v-model="form.angle" required></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field prepend-icon="place" v-model="form.location" label="Location" readonly></v-text-field>
              </v-flex>
            </v-layout>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="dialog = false">Close</v-btn>
          <v-btn color="blue darken-1" flat @click="onPVSubmit">Save</v-btn>
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
        area: '',
        emax: '',
        angle:'',
        location:'Stuttgart'
      }
    }),
    methods: {
        async onPVSubmit(event) {
            this.dialog=false;
            await this.submitPV(this.form.area,this.form.emax,this.form.angle,this.form.location);
            this.$emit('pvSubmitted','pvSubmit');
            this.form.area=this.form.emax=this.form.angle=this.form.location="";
        },
        async submitPV(area, emax, angle, location) {
            let { data } = await axios.get(`http://0.0.0.0:4000/addPV/`+area+`/`+emax+`/`+angle+`/`+location+`/`);
            console.log(data);
        }
    }
  }
</script>