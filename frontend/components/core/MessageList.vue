<template>
  <ul>
    <li v-for="(message, index) in messages" :key="index">
      {{ message }}
    </li>
  </ul>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

@Component
export default class MessageList extends Vue {
  @Prop()
  messages!: string[]
}
</script>
