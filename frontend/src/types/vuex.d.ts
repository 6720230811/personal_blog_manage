declare module 'vuex' {
  export * from 'vuex/types/index'
  
  export function createStore<S>(options: any): Store<S>
  
  // 补充其他可能需要的类型
  export interface Store<S> {
    readonly state: S
    readonly getters: any
    commit: (type: string, payload?: any) => void
    dispatch: (type: string, payload?: any) => Promise<any>
  }
} 