import { MutationTree } from 'vuex'

export const state = () => ({
  snack: '',
})

export type RootState = ReturnType<typeof state>

export const mutations: MutationTree<RootState> = {
  setSnack(state, snack: string) {
    state.snack = snack
  },
}
