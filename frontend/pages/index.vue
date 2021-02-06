<template>
  <v-row>
    <v-col>
      <v-md-preview :text="welcomeText"></v-md-preview>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component({ auth: false })
export default class Home extends Vue {
  welcomeText = `# Welcome to Qurry 🍛
Qurry is the place where students can ask all their questions in an uncomplicated and informal way. 

## Organizational Questions

- Until when can I revoke my lecture enrollment?
- How can I get into the same student dorm room with a friend?

## Exercise/Exam Questions

- Prove $\\forall a,b \\in \\mathbb{N},~ a,b >1 : \\log_a(n) \\in \\Theta(\\log_b(n))$ .
- Explain this C declaration: \`char* (*(*foo[5])(char*))[];\`

## Let's chat 😄

Do you have questions, ideas or feature requests? Please email us to **qurry.info@gmail.com**`
}
</script>

<style scoped></style>
