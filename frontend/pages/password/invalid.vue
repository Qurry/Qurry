<template>
  <v-row>
    <v-col>
      <h1>Password Reset Link Invalid</h1>
      <p>
        This password reset link is invalid, please try again or contact us.
      </p>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component({ middleware: 'guest', auth: false })
export default class InvalidPassword extends Vue {}
</script>
