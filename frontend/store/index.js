export const state = () => ({
  // tags: [
  //   {
  //     id: '1',
  //     name: 'isec',
  //   },
  //   {
  //     id: '2',
  //     name: 'ma3',
  //   },
  //   {
  //     id: '3',
  //     name: 'ti1',
  //   },
  //   {
  //     id: '4',
  //     name: 'abc',
  //   },
  // ],
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
