import { ActionTree, MutationTree } from 'vuex'
import { Profile } from '~/pages/profile/profile.model'
import { Tag, TagCategory } from '~/pages/tags/tag.model'

export const state = () => ({
  tags: <Tag[]>[],
  tagCategories: <TagCategory[]>[],
  profile: <Profile>{},
})

export type RootState = ReturnType<typeof state>

export const mutations: MutationTree<RootState> = {
  SAVE_TAGS: (state, tags: Tag[]) => (state.tags = tags),
  SAVE_TAG_CATEGORIES: (state, tagCategories: TagCategory[]) =>
    (state.tagCategories = tagCategories),
  SAVE_PROFILE: (state, profile: Profile) => (state.profile = profile),
}

export const actions: ActionTree<RootState, RootState> = {
  async fetchTags({ commit }) {
    const tagCategories: TagCategory[] = await this.$axios.$get('/tags')
    const tags: Tag[] = []
    for (const tagCategory of tagCategories) {
      tags.push(...tagCategory.tags)
    }
    commit('SAVE_TAG_CATEGORIES', tagCategories)
    commit('SAVE_TAGS', tags)
  },
  async fetchProfile({ commit }) {
    const profile: Profile = await this.$axios.$get('/profile')
    commit('SAVE_PROFILE', profile)
  },
}
