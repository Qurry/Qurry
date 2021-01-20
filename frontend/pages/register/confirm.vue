<template>
  <v-row>
    <v-col>
      <h1>Email Confirmation</h1>
      <p>Please confirm your HPI email.</p>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component({ auth: false })
export default class ConfirmRegistration extends Vue {}
</script>
