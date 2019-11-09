<template>
    <v-data-table
    :headers="headers"
    :items="buildings"
    class="elevation-1"
  >
    <template v-slot:items="props">
      <td class="text-xs-left" width="10%">{{ props.item.Name }}</td>
    </template>
  </v-data-table>
</template>
<script>
import axios from "axios";
  export default {
    data () {
      return {
        headers: [
          { text: 'Name', value: 'Name' }
        ],
        buildings: []
      }
    },
    mounted() {
      this.getBuildings();
    },
    methods: {
        async getBuildings() {
          let { data } = await axios.get(`http://0.0.0.0:5050/buildings`);
          for (let index = 0; index < data.length; index++) {
            this.buildings.push({"Name":data[index]["BuildingName"]});
          }
        }
    }
  }
</script>
