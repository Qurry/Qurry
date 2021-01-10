<template>
  <div>
    <span>
      – <a class="user-link">{{ post.user.username }}</a> on
      {{ post.createdAt | prettyDateTime }}
    </span>
    <span v-if="isAuthorized">
      <v-btn icon color="secondary" class="action-btn" @click="onEdit">
        <v-icon>mdi-pencil</v-icon> </v-btn
      ><DeleteDialog :object-name="postType" @delete="onDelete" />
    </span>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { User } from '~/pages/users/user.model'

interface Post {
  id: string
  dateTime?: string
  user: User
}

@Component
export default class QuestionDetail extends Vue {
  @Prop()
  post!: Post

  @Prop()
  postType!: string

  isAuthorized = this.$store.state.profile.id === this.post.user.id

  onDelete() {
    this.$emit('delete')
  }

  onEdit() {
    this.$emit('edit')
  }
}
</script>

<style lang="scss" scoped>
.action-btn {
  height: 30px;
  width: 30px;
}
.user-link {
  color: $primary-color;
}
</style>
