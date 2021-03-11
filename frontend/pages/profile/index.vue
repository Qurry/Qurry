<template>
  <v-row>
    <v-col>
      <h1>My Profile</h1>
      <MessageList :messages="errors" />
      <v-simple-table>
        <template v-slot:default>
          <tbody>
            <tr>
              <td>Username</td>
              <td>
                <span v-if="inUsernameEditMode">
                  <v-text-field
                    v-model="newUsername"
                    label="New Username"
                  ></v-text-field>
                  <v-btn color="secondary" @click="editUsername">
                    Submit
                  </v-btn>
                  <v-btn @click="() => (inUsernameEditMode = false)">
                    Cancel
                  </v-btn>
                </span>
                <span v-else>
                  {{ profile.username }}
                  <v-btn icon @click="() => (inUsernameEditMode = true)">
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                </span>
              </td>
            </tr>
            <tr>
              <td>Email</td>
              <td>{{ profile.email }}</td>
            </tr>
            <tr>
              <td>Password</td>
              <td>••••••••</td>
            </tr>
            <tr>
              <td>Score</td>
              <td>{{ profile.score }}</td>
            </tr>
            <tr>
              <td>Register Date</td>
              <td>{{ prettifyDate(profile.registeredAt) }}</td>
            </tr>
            <tr>
              <td>Theme</td>
              <td>light</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import { Profile } from './profile.model'

@Component
export default class Dashboard extends Vue {
  profile: Profile = this.$store.state.profile
  inUsernameEditMode = false
  newUsername = this.profile.username
  errors: string[] = []

  prettifyDate(utcDate: string) {
    const date = new Date(utcDate)
    return (
      date.getDate() + '.' + (date.getMonth() + 1) + '.' + date.getFullYear()
    )
  }

  async editUsername() {
    this.errors = []
    try {
      await this.$axios.patch('/profile/', {
        username: this.newUsername,
      })
      await this.$store.dispatch('fetchProfile')
      this.profile = this.$store.state.profile
      this.inUsernameEditMode = false
    } catch (error) {
      if (error.response.data.errors) {
        this.errors.push(...Object.values(error.response.data.errors as string))
      } else {
        console.log(error)
      }
    }
  }
}
</script>
