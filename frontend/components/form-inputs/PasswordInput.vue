<template>
  <v-text-field
    :value="value"
    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
    :rules="
      creationMode
        ? [
            rules.required,
            rules.minLength,
            rules.maxLength,
            rules.number,
            rules.uppercase,
            rules.lowercase,
          ]
        : [rules.required]
    "
    :type="showPassword ? 'text' : 'password'"
    label="Password"
    color="secondary"
    @click:append="showPassword = !showPassword"
    @input="$emit('input', $event)"
  ></v-text-field>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

@Component
export default class PasswordInput extends Vue {
  @Prop()
  value?: string

  @Prop()
  creationMode?: boolean

  showPassword = false
  rules = {
    required: (value: string) => !!value || 'Required.',
    minLength: (value: string) =>
      value.length >= 10 || 'At least 10 characters.',
    maxLength: (value: string) =>
      value.length <= 100 || 'Maximum 100 characters.',
    number: (value: string) => /\d/.test(value) || 'At least one number.',
    lowercase: (value: string) =>
      /[a-z]/.test(value) || 'At least one lower case letter.',
    uppercase: (value: string) =>
      /[A-Z]/.test(value) || 'At least one upper case letter.',
  }
}
</script>
