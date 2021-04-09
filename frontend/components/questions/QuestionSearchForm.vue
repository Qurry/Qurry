<template>
  <div>
    <v-form @submit.prevent="$emit('submit')">
      <TagSelection
        :selected-tag-ids="search.tagIds"
        @update-selected-tag-ids="updateSelectedTagIds"
      />

      <v-text-field
        v-model.trim="search.words"
        label="Search text"
        append-icon="mdi-magnify"
        outlined
        color="secondary"
        hide-details="true"
        @click:append="$emit('submit')"
      ></v-text-field>

      <div class="filter-row">
        <div class="sort-select">
          <v-select
            v-model="search.orderBy"
            :items="orderByOptions"
            label="Sorted by"
            item-text="text"
            item-value="value"
            color="secondary"
            hide-details="true"
          ></v-select>
        </div>

        <v-checkbox v-model="search.answered" label="With answers"></v-checkbox>

        <v-btn color="secondary" type="submit" class="search-btn">
          Search
        </v-btn>
      </div>
    </v-form>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { QuestionSearch } from '~/pages/questions/question.model'

@Component
export default class QuestionSearchForm extends Vue {
  @Prop()
  search!: QuestionSearch

  orderByOptions = [
    // { text: 'Most Relevant', value: 'relevant' },
    { text: 'Most Votes', value: '-votes' },
    { text: 'Newest', value: '-created_at' },
    { text: 'Oldest', value: 'created_at' },
  ]

  updateSelectedTagIds(selectedTagIds: string[]) {
    this.search.tagIds = selectedTagIds
  }
}
</script>

<style scoped>
.filter-row {
  display: flex;
  margin-bottom: 10px;
}
.search-btn {
  margin-left: auto;
  margin-top: 7px;
}
.sort-select {
  width: 150px;
  margin-right: 10px;
}
</style>
