import { createRouter, createWebHistory } from "vue-router";
import MainPage from "@/views/main/MainPage.vue";

const routes = [
    {
        path: '/', 
        name: 'Main', 
        component: MainPage,
        meta: {
            title: 'Электрополис | Минималистичный магазин'
        }
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router