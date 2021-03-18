<template>
  <v-row>
    <v-col>
      <h1>Confirm Password Reset</h1>
      <p>
        Please confirm the password reset by clicking on the link send to your
        HPI email address.
      </p>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component({ middleware: 'guest', auth: false })
export default class ConfirmPasswordReset extends Vue {}
</script>
