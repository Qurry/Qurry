<template>
  <v-row>
    <v-col>
      <h1 class="mb-3">Tags</h1>
      <v-treeview open-all :items="tagTree">
        <template v-slot:label="{ item }">
          <span>
            <v-chip class="ma-2" :color="item.color ? item.color : '888'">
              {{ item.name }}
            </v-chip>
            {{ item.description }}
          </span>
        </template>
      </v-treeview>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import { Tag } from './tag.model'

@Component
export default class Dashboard extends Vue {
  tagTree: Tag[] = this.$store.state.tagTree
}
</script>
