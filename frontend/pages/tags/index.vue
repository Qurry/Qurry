<template>
  <v-row>
    <v-col>
      <h1 class="mb-3">Tags</h1>
      <v-data-table
        :headers="headers"
        :items="tags"
        :hide-default-footer="true"
        mobile-breakpoint="0"
        class="elevation-1"
      ></v-data-table>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import { Tag } from './tag.model'

@Component
export default class Dashboard extends Vue {
  tags: Tag[] = this.$store.state.tags

  headers = [
    {
      text: 'Name',
      value: 'name',
    },
    {
      text: 'Description',
      value: 'description',
      sortable: false,
    },
  ]
}
</script>
