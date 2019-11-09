<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="600px">
      <template v-slot:activator="{ on }">
        <v-btn color="#227093" dark v-on="on">Add Building</v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="headline">Add Building</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-text-field label="Name*" v-model="form.buildingName" required></v-text-field>
              </v-flex>
            </v-layout>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="dialog = false">Close</v-btn>
          <v-btn color="blue darken-1" flat @click="onBuildingSubmit">Save</v-btn>
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
        buildingName:''
      }
    }),
    methods: {
        async onBuildingSubmit(event) {
            this.dialog=false;
            await this.submitBuilding(this.form.buildingName);
            this.$emit('buildingSubmitted','buildingSubmit');
            this.form.buildingName="";
        },
        async submitBuilding(buildingName) {
            let { data } = await axios.get(`http://0.0.0.0:5050/addBuilding/`+buildingName+`/`);
            console.log(data);
        }
    }
  }
</script>