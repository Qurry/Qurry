<template>
  <div>
    <div v-if="inEditMode">
      <CommentForm
        :comment="editComment"
        class="my-2"
        @submit="onSubmitEdit"
        @cancel="onCancel"
      />
    </div>
    <div v-else>
      <PostContentParser :content="comment.body" mode="body" />
      <PostToolbar
        :post="comment"
        post-type="comment"
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
import { Comment, CreateEditComment } from './../pages/questions/question.model'
import QuestionService from './../services/QuestionService'

@Component
export default class CommentContainer extends Vue {
  inEditMode = false
  @Prop()
  comment!: Comment

  editComment: CreateEditComment = {
    body: '',
  }

  onEdit() {
    this.inEditMode = true
    this.editComment = this.comment
  }

  onSubmitEdit() {
    QuestionService.editComment(this.$axios, this.comment.id, this.editComment)
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
    this.$emit('delete', this.comment.id)
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
  height: 1px;
  background-color: #ccc;
  border: 0;
}
</style>
