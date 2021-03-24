<template>
  <v-app :style="{ background: $vuetify.theme.themes[theme].background }">
    <MessageSnackbar />

    <v-app-bar app color="primary" dark>
      <v-btn to="/" text rounded>Qurry</v-btn>
      <v-spacer></v-spacer>
      <template v-if="$store.state.auth.loggedIn">
        <v-btn to="/questions" text rounded>Questions</v-btn>
        <v-btn to="/tags" text rounded>Tags</v-btn>
        <span>
          {{ userScore }} <v-icon color="#ffb300"> mdi-trophy </v-icon>
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
      <v-container class="container">
        <div v-if="isLoading">
          <LoadingSpinner />
        </div>
        <div v-else>
          <nuxt />
        </div>
      </v-container>
    </v-main>

    <Footer />
  </v-app>
</template>

<script>
import { Vue, Component } from 'nuxt-property-decorator'

@Component
export default class DefaultLayout extends Vue {
  userScore = ''
  isLoading = false

  created() {
    // reload triggered if user logs in
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

  get theme() {
    return this.$vuetify.theme.dark ? 'dark' : 'light'
  }
}
</script>

<style>
/* this has to be global because of vuetify and katex conficting class name .overline */
.v-application .overline {
  font-size: 1em !important;
  line-height: 1.2 !important;
  text-transform: none;
  letter-spacing: 0.08em !important;
}
</style>
