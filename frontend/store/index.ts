import { ActionTree, MutationTree } from 'vuex'
import { Profile } from '~/pages/profile/profile.model'
import { TreeTag, ObjectTag } from '~/pages/tags/tag.model'

export const state = () => ({
  treeTags: <TreeTag[]>[],
  tags: <{ [key: string]: ObjectTag }>{},
  profile: <Profile>{},
})

export type RootState = ReturnType<typeof state>

export const mutations: MutationTree<RootState> = {
  SAVE_TAG_TREE: (state, treeTags: TreeTag[]) => (state.treeTags = treeTags),
  SAVE_TAGS: (state, tags: { [key: string]: ObjectTag }) => (state.tags = tags),
  SAVE_PROFILE: (state, profile: Profile) => (state.profile = profile),
}

const tagColors: { [key: string]: string } = {
  1: '#006909',
  2: '#00179c',
  3: '#007175',
  4: '#640166',
}

function addColors(tag: TreeTag) {
  if (tag.id in tagColors) {
    for (const child of tag.children) {
      child.color = tagColors[tag.id]
    }
  }
  for (const child of tag.children) {
    addColors(child)
  }
}

function createObjectFromTree(
  treeTag: TreeTag,
  parentId: string,
  tagObject: { [key: string]: ObjectTag }
) {
  const childrenIds: string[] = []
  for (const child of treeTag.children) {
    childrenIds.push(child.id)
    createObjectFromTree(child, treeTag.id, tagObject)
  }
  const objectTag: ObjectTag = {
    id: treeTag.id,
    name: treeTag.name,
    description: treeTag.description,
    color: treeTag.color,
    parentId,
    childrenIds,
  }
  tagObject[objectTag.id] = objectTag
}

export const actions: ActionTree<RootState, RootState> = {
  async fetchTags({ commit }) {
    const rawTreeTags: TreeTag[] = await this.$axios.$get('/tags/')
    const treeTags: TreeTag[] = []

    for (const tag of rawTreeTags) {
      tag.color = tagColors['1']
      addColors(tag)
      treeTags.push(tag)
    }

    commit('SAVE_TAG_TREE', treeTags)

    const tags: { [key: string]: ObjectTag } = {}

    for (const tag of treeTags) {
      createObjectFromTree(tag, '-1', tags)
    }

    commit('SAVE_TAGS', tags)
  },
  async fetchProfile({ commit }) {
    const profile: Profile = await this.$axios.$get('/profile/')
    commit('SAVE_PROFILE', profile)
  },
}
