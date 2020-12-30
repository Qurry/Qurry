<template>
  <div class="tags">
    <v-chip
      v-for="tag in selectedTags"
      :key="tag.id"
      class="chip"
      :color="tag.color"
    >
      {{ tag.name }}
    </v-chip>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { Tag } from './../pages/tags/tag.model'

@Component
export default class TagsList extends Vue {
  @Prop()
  tagIds!: string[]

  tags: { [key: string]: Tag } = this.$store.state.tags
  selectedTags: Tag[] = []

  created() {
    for (const tagId of this.tagIds) {
      this.selectedTags.push(this.tags[tagId])
    }
  }
}
</script>

<style scoped>
.tags {
  margin: 3px 0;
  height: 24px;
}
.chip {
  margin-right: 3px;
  height: 25px;
}
</style>
