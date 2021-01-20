<template>
  <v-row>
    <v-col>
      <h1>Email Confirmation Successful!</h1>
      <p>
        Thank you for your email confirmation. You can know
        <NuxtLink to="/login">login</NuxtLink>.
      </p>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component({ middleware: 'guest', auth: false })
export default class SuccessRegistration extends Vue {}
</script>
