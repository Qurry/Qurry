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
    <v-btn color="secondary" small class="mt-2">New Comment</v-btn>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import QuestionService from './../services/QuestionService'
@Component
export default class CommentContainer extends Vue {
  @Prop()
  comments!: Comment[]

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
}
</script>

<style scoped></style>
