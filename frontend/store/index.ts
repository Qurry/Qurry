import { ActionTree, MutationTree } from 'vuex'
import { Profile } from '~/pages/profile/profile.model'
import { TreeNodeTag, ObjectTag } from '~/pages/tags/tag.model'

export const state = () => ({
  tagTree: <TreeNodeTag[]>[],
  tags: <{ [key: string]: ObjectTag }>{},
  profile: <Profile>{},
})

export type RootState = ReturnType<typeof state>

export const mutations: MutationTree<RootState> = {
  SAVE_TAG_TREE: (state, tagTree: TreeNodeTag[]) => (state.tagTree = tagTree),
  SAVE_TAGS: (state, tags: { [key: string]: ObjectTag }) => (state.tags = tags),
  SAVE_PROFILE: (state, profile: Profile) => (state.profile = profile),
}

const tagColors: { [key: string]: string } = {
  1: '#ffadad',
  2: '#ffd6a5',
  3: '#fdffb6',
  4: '#caffbf',
}

function addColors(tag: TreeNodeTag) {
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
  treeNodeTag: TreeNodeTag,
  parentId: string,
  tagObject: { [key: string]: ObjectTag }
) {
  const childrenIds: string[] = []
  for (const child of treeNodeTag.children) {
    childrenIds.push(child.id)
    createObjectFromTree(child, treeNodeTag.id, tagObject)
  }
  const objectTag: ObjectTag = {
    id: treeNodeTag.id,
    name: treeNodeTag.name,
    description: treeNodeTag.description,
    color: treeNodeTag.color,
    parentId,
    childrenIds,
  }
  tagObject[objectTag.id] = objectTag
}

export const actions: ActionTree<RootState, RootState> = {
  async fetchTags({ commit }) {
    const tagTree: TreeNodeTag[] = await this.$axios.$get('/tags/')
    tagTree[0].color = 'gray'
    addColors(tagTree[0])
    commit('SAVE_TAG_TREE', tagTree)

    const tags: { [key: string]: ObjectTag } = {}
    createObjectFromTree(tagTree[0], '0', tags)
    commit('SAVE_TAGS', tags)
  },
  async fetchProfile({ commit }) {
    const profile: Profile = await this.$axios.$get('/profile/')
    commit('SAVE_PROFILE', profile)
  },
}
