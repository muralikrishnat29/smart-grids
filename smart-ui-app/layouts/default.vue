<template>
  <v-app light>
    <v-navigation-drawer
      v-model="drawer"
      :clipped="clipped"
      fixed
      app
      light
      floating
      stateless
      color="#006266"
      value="true"
    >
      <v-list>
        <v-list-tile
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-tile-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title v-text="item.title" />
          </v-list-tile-content>
        </v-list-tile>
        <component-sub-menus></component-sub-menus>
        <v-list-tile
          v-for="(item, i) in secondList"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-tile-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title v-text="item.title" />
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar
      :clipped-left="clipped"
      fixed
      app
      dark
      color="#006266"
    >
      <v-toolbar-side-icon @click="drawer = !drawer" />
      
      <v-btn
        icon
        @click.stop="clipped = !clipped"
      >
      </v-btn>
      <v-btn
        icon
        @click.stop="fixed = !fixed"
      >
      </v-btn>
      <v-toolbar-title v-text="title" />
      <v-spacer />
    </v-toolbar>
    <v-content>
      <v-container>
        <nuxt />
      </v-container>
    </v-content>
    <v-footer
      :fixed="fixed"
      app
    >
      <span>&copy; 2019</span>
    </v-footer>
  </v-app>
</template>

<script>
import componentSubMenus from "./componentSubMenus.vue";
export default {
  components: {
    componentSubMenus
  },
  data() {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      items: [
        {
          icon: 'apps',
          title: 'Welcome',
          to: '/'
        },
        {
          icon: 'insert_chart',
          title: 'Energy Generation Information',
          to: '/generation'
        }
      ],
      secondList: [
        {
          icon: 'local_atm',
          title: 'Pricing Information',
          to: '/pricingComponent'
        },
        {
          icon: 'show_chart',
          title: 'Demand Information',
          to: '/demandComponent'
        },
        {
          icon: 'autorenew',
          title: 'Optimisation',
          to: '/optimise'
        }
      ],
      miniVariant: true,
      right: true,
      rightDrawer: false,
      title: 'Smart Energy Systems',
      color: '#000000'
    }
  }
}
</script>
