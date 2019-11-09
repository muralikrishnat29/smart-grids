<template>
    <v-data-table
    :headers="headers"
    :items="devices"
    class="elevation-1"
  >
    <template v-slot:items="props">
      <td class="text-xs-left" width="10%">{{ props.item.DeviceName }}</td>
      <td class="text-xs-left" width="10%">{{ props.item.DeviceStatus==1? 'Active':'Inactive' }}</td>
      <td class="text-xs-left" width="10%">{{ props.item.EST }}</td>
      <td class="text-xs-left" width="10%">{{ props.item.LET }}</td>
      <td class="text-xs-left" width="10%">{{ props.item.LOT }}</td>
      <td class="text-xs-left" width="10%">{{ props.item.Power }}</td>
      <td class="text-xs-left" width="10%">{{ props.item.StartTime }}</td>
      <td class="text-xs-left" width="10%">{{ props.item.EndTime }}</td>
    </template>
  </v-data-table>
</template>
<script>
import axios from "axios";
  export default {
    data () {
      return {
        headers: [
          { text: 'Device Name', value: 'DeviceName' },
          { text: 'Device Status', value: 'DeviceStatus' },
          { text: 'EST(h)', value: 'EST(h)' },
          { text: 'LET(h)', value: 'LET(h)' },
          { text: 'LOT(h)', value: 'LOT(h)' },
          { text: 'Power(kW)', value: 'Power(kW)' },
          { text: 'Start Time(h)', value: 'StartTime(h)' },
          { text: 'End Time(h)', value: 'EndTime(h)' },
        ],
        devices: []
      }
    },
    props: ['selectedBuilding'],
    mounted() {
      this.getDevices();
    },
    methods: {
        async getDevices() {
          let { data } = await axios.get(`http://0.0.0.0:5050/devices/`+this.selectedBuilding);
          this.devices = data;
          console.log(this.devices);
        }
    }
  }
</script>
