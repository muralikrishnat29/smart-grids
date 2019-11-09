<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="600px">
      <template v-slot:activator="{ on }">
        <v-btn color="#227093" dark v-on="on">Add Wind Turbine</v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="headline">Add Wind Turbine</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-text-field label="RA*" v-model="form.ra" required></v-text-field>
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
          <v-btn color="blue darken-1" flat @click="onWindSubmit">Save</v-btn>
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
        ra: '',
        location:'Stuttgart'
      }
    }),
    methods: {
        async onWindSubmit(event) {
            this.dialog=false;
            await this.submitWind(this.form.ra,this.form.location);
            this.$emit('windSubmitted','windSubmit');
            this.form.ra=this.form.location="";
        },
        async submitWind(ra, location) {
            let { data } = await axios.get(`http://0.0.0.0:4000/addWind/`+ra+`/`+location+`/`);
            console.log(data);
        }
    }
  }
</script>