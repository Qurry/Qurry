<template>
  <div class="tags">
    <v-tooltip v-for="tagId in tagIds" :key="tagId" bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-chip
          v-bind="attrs"
          class="chip"
          :color="tags[tagId].color"
          v-on="on"
          @click="onClick"
        >
          {{ tags[tagId].name }}
        </v-chip>
      </template>
      <span
        >{{ tags[tags[tagId].parentId].name }}:
        {{ tags[tagId].description }}</span
      >
    </v-tooltip>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { ObjectTag } from './../pages/tags/tag.model'

@Component
export default class TagList extends Vue {
  @Prop()
  tagIds!: string[]

  tags: { [key: string]: ObjectTag } = this.$store.state.tags

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
