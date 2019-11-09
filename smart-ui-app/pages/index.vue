<template>
<div>
  <v-carousel
    delimiter-icon="stop"
    prev-icon="mdi-arrow-left"
    next-icon="mdi-arrow-right"
  >
    <v-carousel-item
      v-for="(item,i) in items"
      :key="i"
      :src="item.src"
    ></v-carousel-item>
  </v-carousel>
  <v-card>

        <v-card-title primary-title>
          <div>
            <div class="headline">Smart Energy Grid Management System</div>
            <span class="grey--text">For friendly ecosystem</span>
          </div>
        </v-card-title>

        <v-card-actions>
          <v-btn icon @click="show = !show">
            <v-icon>{{ show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
          </v-btn>
        </v-card-actions>

        <v-slide-y-transition>
          <v-card-text v-show="show">
            In recent years, the terms “Smart Energy” and “Smart Energy Systems” have been used to express an approach that reaches broader than the term “Smart grid”. Where Smart Grids focus primarily on the electricity sector, Smart Energy Systems take an integrated holistic focus on the inclusion of more sectors (electricity, heating, cooling, industry, buildings and transportation) and allows for the identification of more achievable and affordable solutions to the transformation into future renewable and sustainable energy solutions. This paper first makes a review of the scientific literature within the field.
            <br/>Source: <a>https://www.sciencedirect.com/science/article/abs/pii/S0360544217308812</a>
          </v-card-text>
        </v-slide-y-transition>
      </v-card>
  </div>
</template>
<script>
  export default {
    data () {
      return {
        show: true,
        items: [
          {
            src: 'https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg'
          },
          {
            src: 'https://cdn.vuetifyjs.com/images/carousel/sky.jpg'
          },
          {
            src: 'https://cdn.vuetifyjs.com/images/carousel/bird.jpg'
          },
          {
            src: 'https://cdn.vuetifyjs.com/images/carousel/planet.jpg'
          }
        ]
      }
    }
  }
</script>