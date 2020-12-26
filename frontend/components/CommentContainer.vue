<template>
  <div>
    <h3 class="mt-1">
      {{
        comments.length
          ? comments.length + ' Comment' + (comments.length > 1 ? 's' : '')
          : ''
      }}
    </h3>
    <Comment
      v-for="comment in comments"
      :key="comment.id"
      :comment="comment"
      @delete="onDeleteComment"
      @update="$emit('update')"
    />
    <div v-if="inCreateMode">
      <CommentForm
        :comment="createComment"
        class="my-2"
        @submit="onSubmitCreate"
        @cancel="onCancel"
      />
    </div>
    <div v-else>
      <v-btn color="secondary" small class="mt-2" outlined @click="onCreate">
        New Comment
      </v-btn>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { CreateEditComment, Comment } from '../pages/questions/question.model'
import QuestionService from './../services/QuestionService'

@Component
export default class CommentContainer extends Vue {
  inCreateMode = false
  @Prop()
  comments!: Comment[]

  @Prop()
  path!: string

  createComment: CreateEditComment = {
    body: '',
  }

  onDeleteComment(commentId: string) {
    QuestionService.deleteComment(this.$axios, commentId)
      .then((res) => {
        if (res.status === 200) {
          this.$emit('update')
        } else {
          console.log(res)
        }
      })
      .catch((e) => console.log(e))
  }

  onCancel() {
    this.inCreateMode = false
  }

  onCreate() {
    this.inCreateMode = true
  }

  onSubmitCreate() {
    QuestionService.createComment(this.$axios, this.createComment, this.path)
      .then((res) => {
        if (res.status === 201) {
          this.inCreateMode = false
          this.createComment.body = ''
          this.$emit('update')
        } else {
          console.log(res)
        }
      })
      .catch((e) => console.log(e))
  }
}
</script>

<style scoped></style>
