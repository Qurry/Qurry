<template>
  <v-row>
    <v-col>
      <h3>Kategorie</h3>
      <template v-for="tag in tags">
        <v-checkbox
          v-if="tag.parentId === '-1'"
          :key="tag.id"
          v-model="localSelectedTagIds"
          :label="tag.name"
          :value="tag.id"
          hide-details
          class="mt-0"
          @click="updateSelectedTagIds"
        ></v-checkbox>
      </template>
    </v-col>

    <template v-for="tagId in localSelectedTagIds">
      <v-col v-if="tags[tagId].childrenIds.length" :key="tagId + 'child'">
        <h3>{{ tags[tagId].name }}</h3>
        <v-checkbox
          v-for="childTagId in tags[tagId].childrenIds"
          :key="childTagId"
          v-model="localSelectedTagIds"
          :label="tags[childTagId].name"
          :value="tags[childTagId].id"
          hide-details
          class="mt-0"
          @click="updateSelectedTagIds"
        ></v-checkbox>
      </v-col>
    </template>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { ObjectTag } from './../pages/tags/tag.model'

@Component
export default class TagSelection extends Vue {
  @Prop()
  selectedTagIds!: string[]

  localSelectedTagIds: string[] = this.selectedTagIds

  tags: { [key: string]: ObjectTag } = this.$store.state.tags

  updateSelectedTagIds() {
    const tagIds: string[] = []
    for (const tagId of this.localSelectedTagIds) {
      if (
        this.localSelectedTagIds.includes(this.tags[tagId].parentId) ||
        this.tags[tagId].parentId === '-1'
      ) {
        tagIds.push(tagId)
      }
    }
    this.localSelectedTagIds = tagIds
    this.$emit('update-selected-tag-ids', tagIds)
  }
}
</script>

<style scoped></style>
