<template>
  <v-row>
    <v-col>
      <h1>Confirmation Link Invalid</h1>
      <p>This confirmation link is invalid, please contact us.</p>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component({ middleware: 'guest', auth: false })
export default class InvalidRegistration extends Vue {}
</script>
