import { ActionTree, MutationTree } from 'vuex'
import { Profile } from '~/pages/profile/profile.model'
import { Tag, TagCategory } from '~/pages/tags/tag.model'

export const state = () => ({
  tags: <{ [key: string]: Tag }>{},
  tagCategories: <TagCategory[]>[],
  profile: <Profile>{},
})

export type RootState = ReturnType<typeof state>

export const mutations: MutationTree<RootState> = {
  SAVE_TAGS: (state, tags: { [key: string]: Tag }) => (state.tags = tags),
  SAVE_TAG_CATEGORIES: (state, tagCategories: TagCategory[]) =>
    (state.tagCategories = tagCategories),
  SAVE_PROFILE: (state, profile: Profile) => (state.profile = profile),
}

export const actions: ActionTree<RootState, RootState> = {
  async fetchTags({ commit }) {
    const tagCategoryColors: { [key: string]: string } = {
      1: '#ffadad',
      2: '#ffd6a5',
      3: '#fdffb6',
      4: '#caffbf',
      5: '#9bf6ff',
      6: '#a0c4ff',
      7: '#bdb2ff',
      8: '#ffc6ff',
    }
    const rawTagCategories: any[] = await this.$axios.$get('/tags')
    const tagCategories: TagCategory[] = []
    const tags: { [key: string]: Tag } = {}

    for (const rawTagCategory of rawTagCategories) {
      tagCategories.push({
        ...rawTagCategory,
        color: tagCategoryColors[rawTagCategory.id],
      })
    }

    for (const tagCategory of tagCategories) {
      for (const tag of tagCategory.tags) {
        tags[tag.id] = {
          ...tag,
          color: tagCategory.color,
          tagCategoryId: tagCategory.id,
        }
      }
    }
    commit('SAVE_TAG_CATEGORIES', tagCategories)
    commit('SAVE_TAGS', tags)
  },
  async fetchProfile({ commit }) {
    const profile: Profile = await this.$axios.$get('/profile')
    commit('SAVE_PROFILE', profile)
  },
}
