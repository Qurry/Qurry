<template>
  <v-row>
    <v-col>
      <h1>My Profile</h1>
      <v-simple-table>
        <template v-slot:default>
          <tbody>
            <tr>
              <td>Username</td>
              <td>{{ profile.username }}</td>
            </tr>
            <tr>
              <td>Email</td>
              <td>{{ profile.email }}</td>
            </tr>
            <tr>
              <td>Score</td>
              <td>{{ profile.score }}</td>
            </tr>
            <tr>
              <td>Register Date</td>
              <td>{{ profile.registerDate }}</td>
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
}
</script>
