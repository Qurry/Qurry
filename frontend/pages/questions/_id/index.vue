<template>
  <v-row v-if="$fetchState.pending">
    <v-progress-circular
      :size="70"
      :width="7"
      color="primary"
      indeterminate
    ></v-progress-circular>
  </v-row>
  <v-row v-else-if="$fetchState.error">
    <p>Error while fetching question: {{ $fetchState.error.message }}</p>
  </v-row>
  <v-row v-else>
    <v-col>
      <div class="question-container">
        <VotingContainer
          :votes="question.votes"
          :user-vote="question.userVote"
          :path="$route.path"
          class="question-votes-container"
          @update="reloadQuestion"
        />
        <div class="question-body-container">
          <h1 class="mb-3 question-title">
            <PostContentParser :content="question.title" mode="title" />
          </h1>
          <PostContentParser :content="question.body" mode="body" />

          <div>
            <TagsList :tag-ids="question.tagIds" />
            <PostToolbar
              :post="question"
              post-type="question"
              @delete="onDelete"
              @edit="onEdit"
            />
          </div>
          <CommentContainer
            :comments="question.comments"
            :path="$route.path"
            @update="reloadQuestion"
          />
        </div>
      </div>

      <AnswerContainer :answers="question.answers" @update="reloadQuestion" />
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import QuestionService from './../../../services/QuestionService'
import { Answer, DetailQuestion } from './../question.model'

@Component
export default class QuestionDetail extends Vue {
  dialog = false
  // improve this
  question: DetailQuestion = {
    id: '',
    title: '',
    body: '',
    votes: 0,
    userVote: 0,
    createDate: '',
    editDate: '',
    user: {
      id: '',
      username: '',
    },
    tagIds: [],
    answers: [],
    comments: [],
  }

  sortAnswers() {
    this.question.answers.sort((a: Answer, b: Answer) =>
      a.votes! < b.votes! ? 1 : b.votes! < a.votes! ? -1 : 0
    )
  }

  fetch() {
    return Promise.all([
      QuestionService.getQuestion(this.$axios, this.$route.params.id)
        .then((question) => {
          this.question = question
          this.sortAnswers()
        })
        .catch((error) => console.log(error)),
    ])
  }

  onEdit() {
    this.$router.push('/questions/' + this.question.id + '/edit')
  }

  onDelete() {
    QuestionService.deleteQuestion(this.$axios, this.question.id)
      .then((res) => {
        if (res.status === 200) {
          this.$router.push('/questions')
        } else {
          console.log(res)
        }
      })
      .catch((error) => console.log(error))
  }

  reloadQuestion() {
    QuestionService.getQuestion(this.$axios, this.question.id)
      .then((question) => {
        this.question = question
        this.sortAnswers()
      })
      .catch((error) => console.log(error))
  }
}
</script>

<style scoped>
.question-title {
  line-height: 1.2;
}
.question-container {
  display: flex;
}
.question-votes-container {
  width: 50px;
}
.question-body-container {
  flex: 1;
}
</style>
