// @ts-ignore
import { createStore } from 'vuex'

// 定义 State 接口
interface State {
  token: string;
  refreshToken: string;
  user: any;
  isCollapse: boolean;
}

// 定义 CommitFunction 类型
type CommitFunction = (type: string, payload?: any) => void;

// 创建 store
const store = createStore<State>({
  state: {
    token: localStorage.getItem('token') || '',
    refreshToken: localStorage.getItem('refreshToken') || '',
    user: JSON.parse(localStorage.getItem('user') || '{}'),
    isCollapse: false,
  },
  getters: {
    token: (state: State) => state.token,
    refreshToken: (state: State) => state.refreshToken,
    user: (state: State) => state.user,
    isCollapse: (state: State) => state.isCollapse,
    isLoggedIn: (state: State) => !!state.token,
  },
  mutations: {
    SET_TOKEN(state: State, token: string) {
      state.token = token
      localStorage.setItem('token', token)
    },
    SET_REFRESH_TOKEN(state: State, refreshToken: string) {
      state.refreshToken = refreshToken
      localStorage.setItem('refreshToken', refreshToken)
    },
    SET_USER(state: State, user: any) {
      state.user = user
      localStorage.setItem('user', JSON.stringify(user))
    },
    LOGOUT(state: State) {
      state.token = ''
      state.refreshToken = ''
      state.user = {}
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('user')
    },
    TOGGLE_SIDEBAR(state: State) {
      state.isCollapse = !state.isCollapse
    }
  },
  actions: {
    login({ commit }: { commit: CommitFunction }, { token, refreshToken, user }: { token: string, refreshToken: string, user: any }) {
      commit('SET_TOKEN', token)
      if (refreshToken) {
        commit('SET_REFRESH_TOKEN', refreshToken)
      }
      commit('SET_USER', user)
    },
    logout({ commit }: { commit: CommitFunction }) {
      commit('LOGOUT')
    },
    toggleSidebar({ commit }: { commit: CommitFunction }) {
      commit('TOGGLE_SIDEBAR')
    }
  },
  modules: {}
})

export default store 