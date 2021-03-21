<template>
  <div>
    <svg width="50" height="36" viewBox="0 0 36 36">
      <path
        class="vote-arrow"
        :fill="userVote === 1 ? '#e55c44' : '#aaa'"
        d="M2 26h32L18 10 2 26z"
        @click="onVoteUp"
      ></path>
    </svg>
    <div class="vote-number">{{ votes }}</div>
    <svg width="50" height="36" viewBox="0 0 36 36">
      <path
        class="vote-arrow"
        :fill="userVote === -1 ? '#e55c44' : '#aaa'"
        d="M2 10h32L18 26 2 10z"
        @click="onVoteDown"
      ></path>
    </svg>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import QuestionService from '~/services/QuestionService'

@Component
export default class VotingContainer extends Vue {
  @Prop()
  userVote!: number

  @Prop()
  votes!: number

  @Prop()
  path!: string

  onVoteUp() {
    if (this.userVote === 1) {
      this.changeUserVote(0)
    } else {
      this.changeUserVote(1)
    }
  }

  onVoteDown() {
    if (this.userVote === -1) {
      this.changeUserVote(0)
    } else {
      this.changeUserVote(-1)
    }
  }

  changeUserVote(userVote: number) {
    QuestionService.votePost(this.$axios, this.path, userVote)
      .then((_res) => {
        this.$emit('update')
      })
      .catch((e) => console.log(e))
  }
}
</script>

<style scoped>
.vote-arrow {
  cursor: pointer;
}
.vote-number {
  text-align: center;
}
</style>
