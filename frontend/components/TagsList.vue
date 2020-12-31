<template>
  <div class="tags">
    <v-tooltip v-for="tag in selectedTags" :key="tag.id" bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-chip
          v-bind="attrs"
          class="chip"
          :color="tag.color"
          v-on="on"
          @click="onClick"
        >
          {{ tag.name }}
        </v-chip>
      </template>
      <span>{{ tag.tagCategoryName }}: {{ tag.description }}</span>
    </v-tooltip>
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

  onClick() {
    this.$router.push('/tags')
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
.chip:hover {
  cursor: pointer;
}
</style>
