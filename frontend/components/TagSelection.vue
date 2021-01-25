<template>
  <div class="tags">
    <p>{{ selected }}</p>
    <v-row>
      <v-col v-for="tagCategory of tagCategories" :key="tagCategory.id" col="4">
        <h3>{{ tagCategory.name }}</h3>
        <v-checkbox
          v-for="tag of tagCategory.tags"
          :key="tag.id"
          v-model="selected"
          :label="tag.name"
          :value="tag.id"
          hide-details
          class="mt-0"
        ></v-checkbox>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import { TagCategory } from './../pages/tags/tag.model'

@Component
export default class TagSelection extends Vue {
  selected = []
  tagCategories: TagCategory[] = this.$store.state.tagCategories
}
</script>

<style scoped></style>
