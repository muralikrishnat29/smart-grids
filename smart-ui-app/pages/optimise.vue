<template>
<div>
  
    <div class="text-xs-center">
      <v-btn @click="clickOptimise" round color="primary" dark>Optimise</v-btn>
    </div>
    <br/>
    <optimiseData :key="optimiseKey" :v-if="optimiseKey>0"></optimiseData>
</div>
</template>
<script>
import optimiseData from "~/components/optimiseData.vue";
export default {
  components: {
    optimiseData
  },
  data() {
    return {
      optimiseKey: 0,
    };
  },
  methods: {
    async clickOptimise() {
      this.optimiseKey+=1;
    }
  }
  
};
</script>
