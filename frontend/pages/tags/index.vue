<template>
  <v-row>
    <v-col>
      <h1>Tags</h1>
      <p v-for="tag of tags" :key="tag.id">{{ tag.id }} - {{ tag.name }}</p>
      {{ tags }}
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import { Tag } from './tag.model'

@Component
export default class Dashboard extends Vue {
  tags: Tag[] = this.$store.state.tags
  created() {
    console.log('in tags')
  }
}
</script>
