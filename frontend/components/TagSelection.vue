<template>
  <div class="tags">
    {{ selectedTagIds }}
    <v-row>
      <template v-for="tagId in ['1', ...selectedTagIds]">
        <v-col v-if="tags[tagId].childrenIds.length" :key="tagId" col="4">
          <h3>{{ tags[tagId].name }}</h3>
          <v-checkbox
            v-for="childId in tags[tagId].childrenIds"
            :key="childId"
            v-model="selectedTagIds"
            :label="tags[childId].name"
            :value="childId"
            hide-details
            class="mt-0"
          ></v-checkbox>
        </v-col>
      </template>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import { ObjectTag } from './../pages/tags/tag.model'

@Component
export default class TagSelection extends Vue {
  selectedTagIds = []
  tags: ObjectTag[] = this.$store.state.tags
}
</script>

<style scoped></style>
