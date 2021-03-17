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
                  <v-form v-model="isUsernameFormValid">
                    <UsernameInput v-model="newUsername" creation-mode="true" />
                    <v-btn
                      :disabled="!isUsernameFormValid"
                      color="secondary"
                      @click="editUsername"
                    >
                      Submit
                    </v-btn>
                    <v-btn @click="() => (inUsernameEditMode = false)">
                      Cancel
                    </v-btn>
                  </v-form>
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
              <td>
                <span v-if="inPasswordEditMode">
                  <v-form v-model="isPasswordFormValid">
                    <PasswordInput v-model="oldPassword" label="Old Password" />
                    <PasswordInput
                      v-model="newPassword"
                      label="New Password"
                      creation-mode="true"
                    />
                    <v-btn
                      :disabled="!isPasswordFormValid"
                      color="secondary"
                      @click="editPassword"
                    >
                      Submit
                    </v-btn>
                    <v-btn @click="() => (inPasswordEditMode = false)">
                      Cancel
                    </v-btn>
                  </v-form>
                </span>
                <span v-else>
                  ••••••••
                  <v-btn icon @click="() => (inPasswordEditMode = true)">
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                </span>
              </td>
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
  errors: string[] = []
  profile: Profile = this.$store.state.profile

  inUsernameEditMode = false
  isUsernameFormValid = false
  newUsername = this.profile.username

  inPasswordEditMode = false
  isPasswordFormValid = false
  oldPassword = ''
  newPassword = ''

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

  async editPassword() {
    this.errors = []
    try {
      await this.$axios.patch('/profile/', {
        oldPassword: this.oldPassword,
        newPassword: this.newPassword,
      })
      await this.$store.dispatch('fetchProfile')
      this.profile = this.$store.state.profile
      this.inPasswordEditMode = false
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
