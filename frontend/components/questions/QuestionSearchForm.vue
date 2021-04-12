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
        <div class="select">
          <v-select
            v-model="search.orderBy"
            :items="orderByOptions"
            label="Sort by"
            item-text="text"
            item-value="value"
            color="secondary"
            hide-details="true"
          ></v-select>
        </div>

        <div class="select">
          <v-select
            v-model="search.answered"
            :items="answeredOptions"
            label="Filter by"
            item-text="text"
            item-value="value"
            color="secondary"
            hide-details="true"
          ></v-select>
        </div>

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

  answeredOptions = [
    { text: 'All', value: 'all' },
    { text: 'Answered', value: 'true' },
    { text: 'Unanswered', value: 'false' },
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
.select {
  width: 120px;
  margin-right: 10px;
}
</style>
