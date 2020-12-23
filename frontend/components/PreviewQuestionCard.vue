<template>
  <v-card class="mb-3">
    <div class="stats">
      <p>
        {{ question.votes }}
        <v-icon v-if="question.votes > 0" color="green">
          mdi-arrow-up-bold
        </v-icon>
        <v-icon v-else-if="question.votes == 0"> mdi-arrow-right-bold </v-icon>
        <v-icon v-else color="red"> mdi-arrow-down-bold </v-icon>
      </p>
      <p>
        {{ question.answers }}
        <v-icon color="blue"> mdi-comment-text-outline </v-icon>
      </p>
    </div>
    <div class="body">
      <h1 class="title">
        <nuxt-link :to="'/questions/' + question.id" class="question-link">
          <MathJax :data="question.title" />
        </nuxt-link>
      </h1>
      <div class="tags">
        <v-chip v-for="tagId in question.tagIds" :key="tagId" class="mr-2">
          {{ getTagName(tagId) }}
        </v-chip>
      </div>
      <div>
        <p class="footer">
          by
          {{ question.user.username }}
          on
          {{ question.dateTime | prettyDateTime }}
        </p>
      </div>
    </div>
  </v-card>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { PreviewQuestion } from './../pages/questions/question.model'
import { Tag } from './../pages/tags/tag.model'

@Component
export default class QuestionListCard extends Vue {
  @Prop()
  question!: PreviewQuestion[]

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
.stats {
  float: left;
  width: 60px;
  margin-left: 15px;
  margin-top: 15px;
}
.body {
  overflow: hidden;
}
.title {
  margin-top: 5px;
  font-size: 20px;
}
.title:hover {
  text-decoration: underline;
}
.question-link {
  color: #222222;
  text-decoration: none;
}
.tags {
  margin: 5px 0;
  height: 24px;
}
.footer {
  text-align: right;
  color: #888888;
  margin-bottom: 5px;
  margin-right: 10px;
}
.user-link {
  text-decoration: none;
}
.user-link:hover {
  text-decoration: underline;
}
</style>
