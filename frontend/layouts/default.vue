<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-btn to="/" text rounded>Qurry</v-btn>
      <v-spacer></v-spacer>
      <template v-if="loggedIn">
        <v-btn to="/questions" text rounded>Questions</v-btn>
        <v-btn to="/tags" text rounded>Tags</v-btn>
        <v-btn to="/logout" text rounded>Logout</v-btn>
        <v-btn to="/profile" text rounded>Profile</v-btn>
        <span>{{ points }} <v-icon color="orange"> mdi-trophy </v-icon></span>
      </template>
      <template v-else>
        <v-btn to="/login" text rounded>Login</v-btn>
        <v-btn to="/register" text rounded>Register</v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <v-container>
        <div v-if="dataFetched"><nuxt /></div>
        <div v-else>
          <v-progress-circular
            :size="70"
            :width="7"
            color="primary"
            indeterminate
          ></v-progress-circular>
        </div>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { mapState } from 'vuex'
export default {
  data() {
    return {
      points: 145,
      dataFetched: false,
    }
  },
  computed: {
    ...mapState('auth', ['loggedIn']),
  },
  async beforeMount() {
    await this.$store.dispatch('fetchTags')
    this.dataFetched = true
  },
  head: {
    script: [
      {
        src:
          'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-AMS_HTML',
      },
    ],
  },
}
</script>
