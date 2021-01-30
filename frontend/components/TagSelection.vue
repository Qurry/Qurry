<template>
  <div>
    <v-row>
      <template v-for="tagId in ['1', ...selectedTagIds]">
        <v-col
          v-if="tags[tagId].childrenIds.length"
          :key="tagId"
          col="4"
          class="pt-0"
        >
          <h3>{{ tags[tagId].name }}</h3>
          <v-checkbox
            v-for="childId in tags[tagId].childrenIds"
            :key="childId"
            v-model="localSelectedTagIds"
            :label="tags[childId].name"
            :value="childId"
            hide-details
            class="mt-0"
            @click="updateTagIds"
          ></v-checkbox>
        </v-col>
      </template>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { ObjectTag } from './../pages/tags/tag.model'

@Component
export default class TagSelection extends Vue {
  @Prop()
  selectedTagIds!: string[]

  localSelectedTagIds: string[] = []
  tags: ObjectTag[] = this.$store.state.tags

  // hotfix for 'Avoid mutating a prop directly since the value will be overwritten whenever the parent component re-renders.'
  updateTagIds() {
    while (this.selectedTagIds.length) {
      this.selectedTagIds.pop()
    }
    for (const tagId of this.localSelectedTagIds) {
      this.selectedTagIds.push(tagId)
    }
  }
}
</script>

<style scoped></style>
