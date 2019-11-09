<template>
  <v-container>
    <building :key="buildingComponentKey"></building>
    <addBuilding @buildingSubmitted="onBuildingSubmit"></addBuilding>
  </v-container>
</template>
<script>
import addBuilding from "~/components/addBuilding.vue";
import building from "~/components/building.vue";
export default {
  components: {
    addBuilding,
    building
  },
  data() {
    return {
      buildingComponentKey: 0
    };
  },
  methods: {
    async onBuildingSubmit(value) {
      this.buildingComponentKey += 1;
      console.log(value);
    }
  }
};
</script>
