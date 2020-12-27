export const state = () => ({
  tags: [],
  profile: {},
})

export const mutations = {
  SAVE_TAGS: (state, tags) => (state.tags = tags),
  SAVE_PROFILE: (state, profile) => (state.profile = profile),
}

export const actions = {
  async fetchTags({ commit }) {
    const tags = await this.$axios.$get('/tags')
    commit('SAVE_TAGS', tags)
  },
  async fetchProfile({ commit }) {
    const profile = await this.$axios.$get('/profile')
    commit('SAVE_PROFILE', profile)
  },
}
