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
      {{ comment.body }}
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
    this.editComment.body = this.comment.body
  }

  onSubmitEdit() {
    console.log('edit')
    this.inEditMode = false
  }

  onDelete() {
    console.log('delete')
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
