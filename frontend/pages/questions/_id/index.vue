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
            {{ question.title }}
          </h1>

          <v-md-preview :text="question.body" class="pa-0"></v-md-preview>

          <DocumentsList :documents="question.documents" />

          <div>
            <TagList :tag-ids="question.tagIds" />
            <PostToolbar
              :post="question"
              post-type="question"
              @delete="onDelete"
              @edit="onEdit"
            />
            <v-btn
              v-if="question.subscribed"
              small
              color="secondary"
              outlined
              @click="changeSubscriptionTo(false)"
            >
              Unsubscribe <v-icon right dark> mdi-eye-off </v-icon>
            </v-btn>
            <v-btn
              v-else
              small
              color="secondary"
              outlined
              @click="changeSubscriptionTo(true)"
            >
              Subscribe <v-icon right dark> mdi-eye </v-icon>
            </v-btn>
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
    createdAt: '',
    editedAt: '',
    user: {
      id: '',
      username: '',
    },
    subscribed: false,
    tagIds: [],
    answers: [],
    comments: [],
    images: [],
    documents: [],
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
          this.$store.commit(
            'snackbar/setSnack',
            'Successfully deleted question with id ' + res.data.questionId + '.'
          )
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
      })
      .catch((error) => console.log(error))
  }

  async changeSubscriptionTo(subscribe: boolean) {
    try {
      const { data }: { data: DetailQuestion } = await this.$axios.get(
        `/questions/${this.question.id}/?subscribe=${subscribe}`
      )
      this.question = data
    } catch (error) {
      console.log(error)
    }
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
