<template>
  <v-row>
    <v-col>
      <v-md-editor
        :value="value"
        height="400px"
        @input="$emit('input', $event)"
      ></v-md-editor>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

@Component({ auth: false })
export default class PostBodyInput extends Vue {
  @Prop()
  value!: string
}
</script>

<style scoped></style>
