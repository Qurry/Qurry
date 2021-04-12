<template>
  <v-app :style="{ background: $vuetify.theme.themes[theme].background }">
    <MessageSnackbar />

    <MenuBar :user-score="userScore" />

    <v-main>
      <v-container class="layout-container">
        <div v-if="isLoading">
          <LoadingSpinner />
        </div>
        <div v-else>
          <nuxt />
        </div>
      </v-container>
    </v-main>

    <Footer />
  </v-app>
</template>

<script>
import { Vue, Component } from 'nuxt-property-decorator'

@Component
export default class DefaultLayout extends Vue {
  userScore = ''
  isLoading = false

  created() {
    // reload triggered if user logs in
    this.$nuxt.$on('reload', () => {
      this.reload()
    })
  }

  async reload() {
    try {
      this.isLoading = true
      await this.$store.dispatch('fetchTags')
      await this.$store.dispatch('fetchProfile')
      this.userScore = this.$store.state.profile.score.toString()
      this.isLoading = false
    } catch (e) {
      console.log(e)
      await this.$auth.logout()
      this.isLoading = false
    }
  }

  beforeMount() {
    if (this.$store.state.auth.loggedIn) {
      this.reload()
    }
  }

  get theme() {
    return this.$vuetify.theme.dark ? 'dark' : 'light'
  }
}
</script>

<style>
/* this has to be global because of vuetify and katex conficting class name .overline */
.v-application .overline {
  font-size: 1em !important;
  line-height: 1.2 !important;
  text-transform: none;
  letter-spacing: 0.08em !important;
}
.v-application ul,
.v-application ol {
  padding-left: 0px;
}
</style>
