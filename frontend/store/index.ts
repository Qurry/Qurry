import { ActionTree, MutationTree } from 'vuex'
import { Profile } from '~/pages/profile/profile.model'
import { Tag } from '~/pages/tags/tag.model'

export const state = () => ({
  tags: <Tag[]>[],
  profile: <Profile>{},
})

export type RootState = ReturnType<typeof state>

export const mutations: MutationTree<RootState> = {
  SAVE_TAGS: (state, tags: Tag[]) => (state.tags = tags),
  SAVE_PROFILE: (state, profile: Profile) => (state.profile = profile),
}

export const actions: ActionTree<RootState, RootState> = {
  async fetchTags({ commit }) {
    const tags: Tag[] = await this.$axios.$get('/tags')
    commit('SAVE_TAGS', tags)
  },
  async fetchProfile({ commit }) {
    const profile: Profile = await this.$axios.$get('/profile')
    commit('SAVE_PROFILE', profile)
  },
}
