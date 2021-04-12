<template>
  <v-text-field
    :value="value"
    :rules="
      creationMode
        ? [rules.required, rules.minLength, rules.maxLength, rules.allowedChars]
        : [rules.required]
    "
    label="Username"
    required
    color="secondary"
    @input="$emit('input', $event)"
  ></v-text-field>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

@Component
export default class UsernameInput extends Vue {
  @Prop()
  value?: string

  @Prop()
  creationMode?: boolean

  rules = {
    required: (value: string) => !!value || 'Required.',
    minLength: (value: string) => value.length >= 3 || 'At least 3 characters.',
    maxLength: (value: string) =>
      value.length <= 20 || 'Maximum 20 characters.',
    allowedChars: (value: string) =>
      /^[a-zA-Z0-9._-äöüßÄÖÜ]*$/.test(value) ||
      'Only letters, numbers and - _ . are allowed.',
  }
}
</script>
