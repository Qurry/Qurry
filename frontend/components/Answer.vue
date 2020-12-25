<template>
  <div>
    <div v-if="inEditMode">
      <AnswerForm
        :answer="editAnswer"
        class="my-2"
        @submit="onSubmitEdit"
        @cancel="onCancel"
      />
    </div>
    <div v-else>
      {{ answer.body }}
      <PostToolbar
        :post="answer"
        post-type="answer"
        class="toolbar"
        @delete="onDelete"
        @edit="onEdit"
      />
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
  height: 2px;
  background-color: #bbb;
  border: 0;
}
</style>
