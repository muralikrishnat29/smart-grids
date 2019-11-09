<template>
    <v-data-table
    :headers="headers"
    :items="pvComponents"
    class="elevation-1"
  >
    <template v-slot:items="props">
      <td class="text-xs-left" width="10%">{{ props.item.Status==1? 'Active':'Inactive' }}</td>
      <td class="text-xs-left" width="10%">{{ props.item.Area }}</td>
      <td class="text-xs-left" width="10%">{{ props.item.EMax }}</td>
      <td class="text-xs-left" width="10%">{{ props.item.AngleOfModule }}</td>
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
          { text: 'Area', value: 'Area' },
          { text: 'Maximum energy', value: 'EMax' },
          { text: 'Angle of module', value: 'AngleOfModule' },
          { text: 'Location', value: 'Location' }
        ],
        pvComponents: []
      }
    },
    mounted() {
      this.getPVComponents();
    },
    methods: {
        async getPVComponents() {
          let { data } = await axios.get(`http://0.0.0.0:4000/getSolarEnergyData`);
          this.pvComponents = data;
        }
    }
  }
</script>
