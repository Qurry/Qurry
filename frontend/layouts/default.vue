<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-btn to="/" text rounded>Qurry</v-btn>
      <v-spacer></v-spacer>
      <template v-if="loggedIn">
        <v-btn to="/questions" text rounded>Questions</v-btn>
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
        <nuxt />
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
    }
  },
  computed: {
    ...mapState('auth', ['loggedIn']),
  },
}
</script>
