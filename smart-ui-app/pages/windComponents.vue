<template>
    <v-container>
    <windComponent :key="windComponentKey"></windComponent>
    <addWind @windSubmitted="onWindSubmit"></addWind>
  </v-container>
</template>
<script>
import addWind from "~/components/addWind.vue";
import windComponent from "~/components/windComponent.vue";
export default {
    components:{
        addWind,
        windComponent
    },
    data() {
    return {
      windComponentKey: 0
    };
  },
  methods: {
    async onWindSubmit(value) {
      this.windComponentKey += 1;
      console.log(value);
    }
  }
}
</script>
