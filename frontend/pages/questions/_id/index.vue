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
          class="question-votes-container"
          @user-vote-change="changeUserVote"
        />
        <div class="question-body-container">
          <h1 class="mb-3 question-title">
            <MathJax :data="question.title" />
          </h1>
          <p><MathJax :data="question.body" /></p>

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
import { DetailQuestion } from './../question.model'

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

  fetch() {
    return Promise.all([
      QuestionService.getQuestion(this.$axios, this.$route.params.id)
        .then((question) => {
          this.question = question
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

  changeUserVote(userVote: number) {
    QuestionService.voteQuestion(this.$axios, this.question.id, userVote)
      .then((_res) => {
        this.reloadQuestion()
      })
      .catch((error) => console.log(error))
  }

  reloadQuestion() {
    QuestionService.getQuestion(this.$axios, this.question.id)
      .then((question) => {
        this.question = question
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
