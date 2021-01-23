<template>
  <v-row>
    <v-col>
      <h1>Welcome to Qurry 🍛</h1>
      <p>
        Qurry is the place where students can ask all their questions in an
        uncomplicated and informal way.
      </p>

      <h2>Organisational Questions</h2>

      <ul>
        <li>Until when can I revoke my lecture enrollment?</li>
        <li>How can I get into the same student dorm room with a friend?</li>
      </ul>

      <h2>Exercise/Exam Questions</h2>

      <ul>
        <li>Prove that L is co-RE complete.</li>
      </ul>
      <br />
      <h2>Let's chat 😄</h2>
      <p>
        Do you have questions, ideas or feature requests? Please send us an
        email to <strong> qurry.info@gmail.com </strong>
      </p>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component({ auth: false })
export default class Dashboard extends Vue {}
</script>
