<template>
  <v-row>
    <v-col>
      <h1 class="mb-3">Tags</h1>
      <div
        v-for="tagCategory in tagCategories"
        :key="tagCategory.id"
        class="mt-3"
      >
        <h2 :style="{ backgroundColor: tagCategory.color }">
          {{ tagCategory.name }}
        </h2>
        <p>{{ tagCategory.description }}</p>
        <v-data-table
          :headers="headers"
          :items="tagCategory.tags"
          :hide-default-footer="true"
          mobile-breakpoint="0"
          class="elevation-1"
        ></v-data-table>
      </div>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import { TagCategory } from './tag.model'

@Component
export default class Dashboard extends Vue {
  tagCategories: TagCategory[] = this.$store.state.tagCategories

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
