<template>
  <v-app>
    <MessageSnackbar />

    <v-app-bar app color="primary" dark>
      <v-btn to="/" text rounded>Qurry</v-btn>
      <v-spacer></v-spacer>
      <template v-if="$store.state.auth.loggedIn">
        <v-btn to="/logout" text rounded>Logout</v-btn>
        <v-btn to="/questions" text rounded>Questions</v-btn>
        <v-btn to="/tags" text rounded>Tags</v-btn>
        <v-btn to="/users" text rounded>Users</v-btn>
        <v-btn to="/profile" text rounded>Profile</v-btn>
        <span>
          {{ userScore }} <v-icon color="accent"> mdi-trophy </v-icon>
        </span>
      </template>
      <template v-else>
        <v-btn to="/login" text rounded>Login</v-btn>
        <v-btn to="/register" text rounded>Register</v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <v-container>
        <div v-if="isLoading">
          <v-progress-circular
            :size="70"
            :width="7"
            color="primary"
            indeterminate
          ></v-progress-circular>
        </div>
        <div v-else>
          <nuxt />
        </div>
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component({
  head: {
    script: [
      {
        src:
          'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-AMS_HTML',
      },
    ],
  },
})
export default class DefaultLayout extends Vue {
  userScore = ''
  isLoading = false

  created() {
    this.$nuxt.$on('reload', () => {
      this.reload()
    })
  }

  async reload() {
    try {
      this.isLoading = true
      await this.$store.dispatch('fetchTags')
      await this.$store.dispatch('fetchProfile')
      this.userScore = this.$store.state.profile.score.toString()
      this.isLoading = false
    } catch (e) {
      console.log(e)
      await this.$auth.logout()
      this.isLoading = false
    }
  }

  beforeMount() {
    if (this.$store.state.auth.loggedIn) {
      this.reload()
    }
  }
}
</script>
