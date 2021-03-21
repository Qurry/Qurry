<template>
  <v-text-field
    :value="value"
    :rules="[rules.required, rules.email]"
    label="Email"
    required
    color="secondary"
    @input="$emit('input', $event)"
  ></v-text-field>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

@Component
export default class EmailInput extends Vue {
  @Prop()
  value?: string

  rules = {
    required: (value: string) => !!value || 'Required.',
    email: (value: string) => {
      const pattern = /^[\w.-]*@([\w.-]+\.)?(hpi\.de|hpi\.uni-potsdam\.de)$/
      return pattern.test(value) || 'Please use an HPI email.'
    },
  }
}
</script>
