<template>
  <v-row>
    <v-col>
      <h1>E-Mail bestätigen</h1>
      <p>Bitte bestätige deine HPI E-Mail.</p>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component({ auth: false })
export default class ConfirmRegistration extends Vue {}
</script>
