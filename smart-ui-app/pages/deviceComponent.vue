<template>
    <v-container>
        <building @buildingSelected="buildingChange"></building>
        <devices :key="deviceUpdateKey" v-bind:selectedBuilding="selectedBuildingId" v-if="selectedBuildingId>0"></devices>
        <addDevice :key="buildingSelectedKey" @deviceSubmitted="onDeviceSubmit" v-bind:selectedBuilding="selectedBuildingId" v-if="selectedBuildingId>0"></addDevice>
    </v-container>
</template>
<script>
import building from "~/components/buildingList.vue";
import devices from "~/components/devices.vue";
import addDevice from "~/components/addDevice.vue";
export default {
    components:{
        building,
        devices,
        addDevice
    },
    data() {
        return {
            buildingSelectedKey: 0,
            deviceUpdateKey: 0,
            selectedBuildingId: {}
        }
    },
    methods: {
    async buildingChange(value) {
      this.buildingSelectedKey += 1;
      this.deviceUpdateKey+=1;
      this.selectedBuildingId = value.Id;
    },
    async onDeviceSubmit(event) {
      this.deviceUpdateKey+=1;
    }
  }
}
</script>