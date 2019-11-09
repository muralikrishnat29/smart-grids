<template>
    <v-data-table
    :headers="headers"
    :items="windComponents"
    class="elevation-1"
  >
    <template v-slot:items="props">
      <td class="text-xs-left" width="10%">{{ props.item.Status==1? 'Active':'Inactive' }}</td>
      <td class="text-xs-left" width="10%">{{ props.item.Ra }}</td>
      <td class="text-xs-left" width="10%">{{ props.item.Location }}</td>
    </template>
  </v-data-table>
</template>
<script>
import axios from "axios";
  export default {
    data () {
      return {
        headers: [
          { text: 'Status', value: 'Status' },
          { text: 'Ra', value: 'Ra' },
          { text: 'Location', value: 'Location' }
        ],
        windComponents: []
      }
    },
    mounted() {
      this.getWindComponents();
    },
    methods: {
        async getWindComponents() {
          let { data } = await axios.get(`http://0.0.0.0:4000/getWindEnergyData`);
          this.windComponents = data;
        }
    }
  }
</script>
