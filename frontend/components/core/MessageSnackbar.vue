<template>
  <v-snackbar v-model="show">
    {{ message }}
    <v-btn text color="primary" @click.native="show = false">Close</v-btn>
  </v-snackbar>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component
export default class MessageSnackbar extends Vue {
  show = false
  message = ''

  created() {
    this.$store.watch(
      (state) => state.snackbar.snack,
      () => {
        const msg = this.$store.state.snackbar.snack
        if (msg !== '') {
          this.show = true
          this.message = this.$store.state.snackbar.snack
          this.$store.commit('snackbar/setSnack', '')
        }
      }
    )
  }
}
</script>
