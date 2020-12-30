<template>
  <v-row>
    <v-col>
      <h1>Dashboard</h1>
      <p>Willkommen auf Qurry - dem StackOverflow für die Uni</p>
      <h2>Heiße Fragen</h2>
      <p>Es gibt noch keine heißen Fragen.</p>
      <h2>Meine Fragen</h2>
      <p>Du hast noch keine Frage gestellt.</p>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component({ auth: false })
export default class Dashboard extends Vue {}
</script>
