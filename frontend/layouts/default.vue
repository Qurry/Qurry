<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-btn to="/" text rounded>Qurry</v-btn>
      <v-spacer></v-spacer>
      <v-btn to="/questions" text rounded>Fragen</v-btn>
      <v-btn to="/profile" text rounded>Profil</v-btn>
      <span>{{ points }} <v-icon color="orange"> mdi-trophy </v-icon></span>
    </v-app-bar>

    <v-main>
      <v-container>
        <nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component
export default class DefaultLayout extends Vue {
  points = 145
}
</script>
