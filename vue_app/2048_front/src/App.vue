
<script lang="ts">
import UserCard from './components/UserCard.vue'

export default {
  components: {UserCard},
  data() {
    return {
      BACK_URL: "http://localhost:8005",
      MAX_VALUE: 2048,
      curr_score: -1,

      grid: [
        [0, 0, 0, 0],
        [0, 2, 0, 0],
        [0, 0, 4, 0],
        [0, 0, 0, 0]
      ]
    }
  },
  methods: {

  },

  computed: {}
}
</script>

<template>
  <header>
    <h1>2048</h1>
  </header>

  <main>
    <UserCard :BACK_URL="BACK_URL"/>
    <div>
      <div v-for="(row, idx) in grid" :key="idx">
        <div v-for="(num, idx1) in row" :key="idx1" style="display: inline-flex; margin: 3px; padding: 3px;">
          <div v-if="num!=0" style="height: 25px; width: 25px; background-color: green;">{{ num }}</div>
          <div v-else style="height: 25px; width: 25px; background-color: aqua;"></div>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>

</style>
