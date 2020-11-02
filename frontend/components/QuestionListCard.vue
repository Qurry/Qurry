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
          {{ question.title }}
        </nuxt-link>
      </h1>
      <div class="tags">
        <v-chip v-for="tag in question.tags" :key="tag.id" class="mr-2">
          {{ tag.name }}
        </v-chip>
      </div>
      <div>
        <p class="footer">
          von
          <nuxt-link :to="'/users/' + question.user.id" class="user-link">
            {{ question.user.name }}
          </nuxt-link>
          am
          <!-- {{ toPrettyDateTime(question.dateTime) }} -->
        </p>
      </div>
    </div>
  </v-card>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { PreviewQuestion } from './../pages/questions/question.model'

@Component
export default class QuestionListCard extends Vue {
  @Prop()
  question!: PreviewQuestion[]

  toPrettyDateTime(rawDateTime: string): string {
    const prettyDateTime =
      rawDateTime.slice(8, 10) +
      '.' +
      rawDateTime.slice(5, 7) +
      '.' +
      rawDateTime.slice(0, 4) +
      ' um ' +
      rawDateTime.slice(11, 16)
    return prettyDateTime
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
