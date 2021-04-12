<template>
  <v-app-bar app color="primary" dark>
    <NuxtLink to="/">
      <v-img
        class="mx-2"
        src="/static/icon-180x180.png"
        max-height="35"
        max-width="35"
        contain
      >
      </v-img>
    </NuxtLink>
    <v-spacer></v-spacer>
    <template v-if="$store.state.auth.loggedIn">
      <v-btn to="/questions" text rounded>Questions</v-btn>
      <v-btn to="/tags" text rounded>Tags</v-btn>
      <span>
        {{ userScore }} <v-icon color="#ffb300"> mdi-trophy </v-icon>
      </span>
      <NotificationMenu />
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
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

@Component
export default class MessageList extends Vue {
  @Prop()
  userScore = ''
}
</script>
