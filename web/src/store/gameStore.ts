import {create} from "zustand";

interface IGameStore {
    life: number,
    setLife: (life) => void;
    score: number,
    setScore: (score) => void;
}

export const useGameStore = create<IGameStore>()((set) => ({
    life: 3,
    score: 0,
    setLife: (life) => {
        set((state) => {
            return {
                life: life,
                score: state.score
            }
        })
    },
    setScore: (score) => {
        set((state) => {
            return {
                life: state.life,
                score: score
            }
        })
    }
}))