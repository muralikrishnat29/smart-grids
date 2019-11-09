<template>
  <v-container>
    <battery :key="batteryComponentKey"></battery>
    <updateBattery @batteryUpdated="onBatterySubmit"></updateBattery>
  </v-container>
</template>
<script>
import updateBattery from "~/components/updateBattery.vue";
import battery from "~/components/battery.vue";
export default {
  components: {
    updateBattery,
    battery
  },
  data() {
    return {
      batteryComponentKey: 0
    };
  },
  methods: {
    async onBatterySubmit(value) {
      this.batteryComponentKey += 1;
      console.log(value);
    }
  }
};
</script>
