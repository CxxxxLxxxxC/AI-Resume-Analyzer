import { createStore } from 'vuex'

export default createStore({
    state: {
        resumeData: null
    },
    mutations: {
        setResumeData(state, data) {
            state.resumeData = data
        }
    },
    actions: {
        updateResumeData({ commit }, data) {
            commit('setResumeData', data)
        }
    }
})