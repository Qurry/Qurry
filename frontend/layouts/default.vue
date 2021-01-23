<template>
  <v-app>
    <MessageSnackbar />

    <v-app-bar app color="primary" dark>
      <v-btn to="/" text rounded>Qurry</v-btn>
      <v-spacer></v-spacer>
      <template v-if="$store.state.auth.loggedIn">
        <v-btn to="/questions" text rounded>Questions</v-btn>
        <v-btn to="/tags" text rounded>Tags</v-btn>
        <span>
          {{ userScore }} <v-icon color="accent"> mdi-trophy </v-icon>
        </span>
        <v-menu offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on">
              <v-icon>mdi-menu</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item>
              <v-btn to="/profile" text rounded>Profile</v-btn>
            </v-list-item>
            <v-list-item>
              <v-btn to="/users" text rounded>Users</v-btn>
            </v-list-item>
            <v-list-item>
              <v-btn to="/logout" text rounded>Logout</v-btn>
            </v-list-item>
          </v-list>
        </v-menu>
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

    <Footer />
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

  items = [
    { title: 'Click Me' },
    { title: 'Click Me' },
    { title: 'Click Me' },
    { title: 'Click Me 2' },
  ]

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
