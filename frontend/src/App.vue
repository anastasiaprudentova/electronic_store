<template>
  <div id="app">
    <LayoutHeader />
    <main>
      <router-view />
    </main>
    <LayoutFooter />
    <div class="toast-container" id="toast-container"></div>
  </div>
</template>

<script>
import LayoutHeader from "./components/LayoutHeader.vue";
import LayoutFooter from "./components/LayoutFooter.vue";

export default {
  components: { LayoutHeader, LayoutFooter },
  watch: {
    $route(to, from) {
      if (to.meta.title) {
        document.title = to.meta.title
      } else {
        document.title = 'Электрополис | Минималистичный магазин'
      }
    }
  },
  mounted() {
    if (this.$route.meta.title) {
      document.title = this.$route.meta.title
    }
  }
}
</script>