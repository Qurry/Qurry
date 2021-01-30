import { ActionTree, MutationTree } from 'vuex'
import { Profile } from '~/pages/profile/profile.model'
import { Tag } from '~/pages/tags/tag.model'

export const state = () => ({
  tagTree: <Tag[]>[],
  profile: <Profile>{},
})

export type RootState = ReturnType<typeof state>

export const mutations: MutationTree<RootState> = {
  SAVE_TAG_TREE: (state, tagTree: Tag[]) => (state.tagTree = tagTree),
  SAVE_PROFILE: (state, profile: Profile) => (state.profile = profile),
}

const tagColors: { [key: string]: string } = {
  1: '#ffadad',
  2: '#ffd6a5',
  3: '#fdffb6',
  4: '#caffbf',
}

function addColors(tag: Tag) {
  if (tag.id in tagColors) {
    for (const child of tag.children) {
      child.color = tagColors[tag.id]
    }
  }
  for (const child of tag.children) {
    addColors(child)
  }
}

export const actions: ActionTree<RootState, RootState> = {
  async fetchTags({ commit }) {
    const tagTree = await this.$axios.$get('/tags/')
    addColors(tagTree[0])
    commit('SAVE_TAG_TREE', tagTree)
  },
  async fetchProfile({ commit }) {
    const profile: Profile = await this.$axios.$get('/profile/')
    commit('SAVE_PROFILE', profile)
  },
}
