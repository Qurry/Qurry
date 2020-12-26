<template>
  <div class="tags">
    <v-chip v-for="tagId in tagIds" :key="tagId" class="chip">
      {{ getTagName(tagId) }}
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

  tags: Tag[] = this.$store.state.tags

  getTagName(tagId: string): string {
    for (const tag of this.tags) {
      if (tag.id === tagId) {
        return tag.name
      }
    }
    return ''
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
