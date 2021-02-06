<template>
  <v-row>
    <v-col>
      <v-md-editor v-model="body" height="400px"></v-md-editor>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component({ auth: false })
export default class PostBodyInput extends Vue {
  body = ''
}
</script>

<style scoped></style>
