<template>
  <div>
    <span>
      – <a class="user-link">{{ post.user.username }}</a> 13 weeks ago
      <!-- on {{ post.dateTime ? post.dateTime : '' }} -->
    </span>
    <span>
      <v-btn icon color="secondary" class="action-btn" @click="onEdit">
        <v-icon>mdi-pencil</v-icon> </v-btn
      ><v-dialog v-model="dialog" persistent max-width="290">
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            color="secondary"
            v-bind="attrs"
            class="action-btn"
            v-on="on"
          >
            <v-icon>mdi-trash-can-outline</v-icon>
          </v-btn>
        </template>
        <v-card>
          <v-card-title class="headline">
            Do you really want to delete this {{ postType }}?
          </v-card-title>
          <v-card-text>This action can't be undone.</v-card-text>
          <v-card-actions>
            <v-btn color="error" @click="onDelete"> Delete </v-btn>
            <v-spacer></v-spacer>
            <v-btn color="#ddd" @click="dialog = false"> Cancel </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </span>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { User } from './../pages/questions/question.model'

interface Post {
  id: string
  dateTime?: string
  user: User
}

@Component
export default class QuestionDetail extends Vue {
  dialog = false
  @Prop()
  post!: Post

  @Prop()
  postType!: string

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
