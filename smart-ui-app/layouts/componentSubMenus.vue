<template>
  <v-list-group prepend-icon="group_work" value="true">
    <template v-slot:activator>
      <v-list-tile>
        <v-list-tile-title>Components Management</v-list-tile-title>
      </v-list-tile>
    </template>
    <v-list-group no-action sub-group value="true">
      <template v-slot:activator>
        <v-list-tile>
          <v-list-tile-title>Supply Side</v-list-tile-title>
        </v-list-tile>
      </template>

      <v-list-tile v-for="(supply, i) in supplySide" :key="i" :to="supply[2]">
        <v-list-tile-action>
          <v-icon v-text="supply[1]"></v-icon>
        </v-list-tile-action>
        <v-list-tile-title v-text="supply[0]"></v-list-tile-title>
      </v-list-tile>
    </v-list-group>

    <v-list-group sub-group no-action>
      <template v-slot:activator>
        <v-list-tile>
          <v-list-tile-title>Demand Side</v-list-tile-title>
        </v-list-tile>
      </template>
      <v-list-tile v-for="(demand, i) in demandSide" :key="i" :to="demand[2]">
        <v-list-tile-action>
          <v-icon v-text="demand[1]"></v-icon>
        </v-list-tile-action>
        <v-list-tile-title v-text="demand[0]"></v-list-tile-title>
      </v-list-tile>
    </v-list-group>
  </v-list-group>
</template>
<script>
export default {
  data() {
    return {
      supplySide: [
        ["Wind Turbine", "toys", "/windComponents"],
        ["Solar Panel", "brightness_5", "/pvComponents"],
        ["Battery", "battery_charging_full", "/batteryComponent"]
      ],
      demandSide: [
        ["Building", "account_balance", "/buildingComponent"],
        ["Device", "devices", "/deviceComponent"]
      ]
    };
  }
};
</script>
