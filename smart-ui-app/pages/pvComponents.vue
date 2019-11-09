<template>
  <v-container>
    <pvComponent :key="pvComponentKey"></pvComponent>
    <addPV @pvSubmitted="onPVSubmit"></addPV>
  </v-container>
</template>
<script>
import addPV from "~/components/addPV.vue";
import pvComponent from "~/components/pvComponent.vue";
export default {
  components: {
    addPV,
    pvComponent
  },
  data() {
    return {
      pvComponentKey: 0
    };
  },
  methods: {
    async onPVSubmit(value) {
      this.pvComponentKey += 1;
      console.log(value);
    }
  }
};
</script>
