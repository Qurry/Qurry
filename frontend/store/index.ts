import { ActionTree, MutationTree } from 'vuex'
import { Profile } from '~/pages/profile/profile.model'
import { TreeTag, ObjectTag } from '~/pages/tags/tag.model'
import {
  PreviewQuestion,
  QuestionSearch,
  Notification,
} from '~/pages/questions/question.model'

export const state = () => ({
  isLoadingQuestions: false,
  isLoadingNecessaryData: false,
  questions: <PreviewQuestion[]>[],
  numOfQuestions: 0,
  numOfUnreadNotifications: 0,
  unreadNotifications: <Notification[]>[],
  treeTags: <TreeTag[]>[],
  tags: <{ [key: string]: ObjectTag }>{},
  profile: <Profile>{},
})

export type RootState = ReturnType<typeof state>

export const mutations: MutationTree<RootState> = {
  SET_IS_LOADING_QUESTIONS: (state, isLoading: boolean) =>
    (state.isLoadingQuestions = isLoading),
  SET_IS_LOADING_NECESSARY_DATA: (state, isLoading: boolean) =>
    (state.isLoadingNecessaryData = isLoading),
  SET_QUESTIONS: (state, questions: PreviewQuestion[]) =>
    (state.questions = questions),
  SET_NUM_OF_QUESTIONS: (state, numOfQuestions: number) =>
    (state.numOfQuestions = numOfQuestions),
  SET_NUM_OF_UNREAD_NOTIFICATIONS: (state, numOfUnreadNotifications: number) =>
    (state.numOfUnreadNotifications = numOfUnreadNotifications),
  SET_UNREAD_NOTIFICATIONS: (state, unreadNotifications: Notification[]) =>
    (state.unreadNotifications = unreadNotifications),
  SET_TAG_TREE: (state, treeTags: TreeTag[]) => (state.treeTags = treeTags),
  SET_TAGS: (state, tags: { [key: string]: ObjectTag }) => (state.tags = tags),
  SET_PROFILE: (state, profile: Profile) => (state.profile = profile),
}

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

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
  async getQuestions({ commit }, search: QuestionSearch) {
    commit('SET_IS_LOADING_QUESTIONS', true)
    const {
      data,
    }: {
      data: { count: number; questions: PreviewQuestion[] }
    } = await this.$axios.get(
      `/questions/?limit=${search.limit}\
&offset=${(search.page - 1) * search.limit}\
&words=${search.words}\
&order_by=${search.orderBy}\
&tag_ids=${search.tagIds.join()}\
&answered=${search.answered}`
    )
    commit('SET_QUESTIONS', data.questions)
    commit('SET_NUM_OF_QUESTIONS', data.count)
    commit('SET_IS_LOADING_QUESTIONS', false)
  },
  async fetchTags({ commit }) {
    const rawTreeTags: TreeTag[] = await this.$axios.$get('/tags/')
    const treeTags: TreeTag[] = []

    for (const tag of rawTreeTags) {
      tag.color = tagColors['1']
      addColors(tag)
      treeTags.push(tag)
    }

    commit('SET_TAG_TREE', treeTags)

    const tags: { [key: string]: ObjectTag } = {}

    for (const tag of treeTags) {
      createObjectFromTree(tag, '-1', tags)
    }

    commit('SET_TAGS', tags)
  },
  async fetchProfile({ commit }) {
    const profile: Profile = await this.$axios.$get('/profile/')
    commit('SET_PROFILE', profile)
  },
  async getNotifications({ commit }) {
    const data: {
      count: number
      notifications: Notification[]
    } = await this.$axios.$get('/notifications/unread/')
    commit('SET_NUM_OF_UNREAD_NOTIFICATIONS', data.count)
    commit('SET_UNREAD_NOTIFICATIONS', data.notifications)
  },
  async updateNotificationStatus({ commit }) {
    while (true) {
      const data: {
        count: number
      } = await this.$axios.$get('/notifications/status/')
      commit('SET_NUM_OF_UNREAD_NOTIFICATIONS', data.count)
      await delay(10000)
    }
  },
}
