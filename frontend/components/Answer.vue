<template>
  <div>
    <div class="answer-container">
      <VotingContainer
        :votes="answer.votes"
        :user-vote="answer.userVote"
        :path="'/answers/' + answer.id"
        class="answer-votes-container"
        @update="$emit('update')"
      />
      <div class="answer-body-container">
        <div v-if="inEditMode">
          <AnswerForm
            :answer="editAnswer"
            class="my-2"
            @submit="onSubmitEdit"
            @cancel="onCancel"
          />
        </div>
        <div v-else>
          <PostContentParser
            :content="answer.body"
            mode="body"
            :images="answer.images"
          />
          <PostToolbar
            :post="answer"
            post-type="answer"
            class="toolbar"
            @delete="onDelete"
            @edit="onEdit"
          />
          <CommentContainer
            :comments="answer.comments"
            :path="'/answers/' + answer.id"
            @update="$emit('update')"
          />
        </div>
      </div>
    </div>
    <hr class="divider" />
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { Answer, CreateEditAnswer } from './../pages/questions/question.model'
import QuestionService from './../services/QuestionService'

@Component
export default class AnswerDiv extends Vue {
  inEditMode = false
  @Prop()
  answer!: Answer

  editAnswer: CreateEditAnswer = {
    body: '',
    images: [],
    documents: [],
  }

  onEdit() {
    this.inEditMode = true
    this.editAnswer = this.answer
  }

  onSubmitEdit() {
    QuestionService.editAnswer(this.$axios, this.answer.id, this.editAnswer)
      .then((res) => {
        if (res.status === 200) {
          this.inEditMode = false
          this.$emit('update')
        } else {
          console.log(res)
        }
      })
      .catch((e) => console.log(e))
  }

  onDelete() {
    this.$emit('delete', this.answer.id)
  }

  onCancel() {
    this.inEditMode = false
  }
}
</script>

<style scoped>
.action-icon {
  cursor: pointer;
}
.toolbar {
  display: inline;
}
.divider {
  margin: 15px 0;
  height: 1px;
  background-color: #ccc;
  border: 0;
}
.answer-container {
  display: flex;
}
.answer-votes-container {
  width: 50px;
}
.answer-body-container {
  flex: 1;
  /* margin-bottom: 25px; */
}
</style>
