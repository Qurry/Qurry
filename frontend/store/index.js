export const state = () => ({
  tags: [],
})

export const mutations = {
  SAVE_TAGS: (state, tags) => (state.tags = tags),
}

export const actions = {
  async fetchTags({ commit }) {
    const tags = await this.$axios.$get('/tags')
    commit('SAVE_TAGS', tags)
  },
}
