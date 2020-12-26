<template>
  <v-row>
    <v-col>
      <h1 class="mb-3">Top 10 Users</h1>
      <v-data-table
        :headers="headers"
        :items="users"
        :hide-default-footer="true"
        mobile-breakpoint="0"
        class="elevation-1"
      ></v-data-table>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component
export default class Dashboard extends Vue {
  users = [
    {
      username: 'Abdu',
      score: 672,
    },
    {
      username: 'Emma',
      score: 453,
    },
    {
      username: 'Tom',
      score: 134,
    },
  ]

  headers = [
    {
      text: 'Username',
      value: 'username',
      sortable: false,
    },
    {
      text: 'Score',
      value: 'score',
      sortable: false,
    },
  ]
}
</script>
