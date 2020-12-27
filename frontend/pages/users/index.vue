<template>
  <v-row>
    <v-col>
      <h1>Users</h1>
      <v-list>
        <template v-for="(user, index) in users">
          <v-list-item :key="index" class="pl-0">
            <v-list-item-avatar>
              <v-img v-if="user.image" :src="apiUrl + user.image"></v-img>
              <v-img v-else src="/default-profile-image.png"></v-img>
            </v-list-item-avatar>

            <v-list-item-content>
              <v-list-item-title>{{ user.username }}</v-list-item-title>
              <v-list-item-subtitle>{{ user.score }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-list>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import UserService from '../../services/UserService'
import { User } from './user.model'

@Component
export default class Dashboard extends Vue {
  users: User[] = []
  apiUrl = process.env.API_URL

  fetch() {
    return Promise.all([
      UserService.getUsers(this.$axios)
        .then((users) => {
          this.users = users.sort((a: User, b: User) =>
            a.score! < b.score! ? 1 : b.score! < a.score! ? -1 : 0
          )
        })
        .catch((e) => console.log(e)),
    ])
  }
}
</script>
