<script lang="ts">
import UserCard from './components/UserCard.vue'
import GameGrid from "./components/GameGrid.vue";

export default {
  components: {UserCard, GameGrid},
  data() {
    return {
      BACK_URL: "http://localhost:8005",
      MAX_VALUE: 2048,
      GAME_SIZE: 4,
      curr_score: 0,
    }
  },
  methods: {
    addScore(value: number) {
      this.curr_score += value;
    }
  },

  computed: {}
}
</script>

<template>
  <main class="center-block">
    <h1>2048</h1>
    <UserCard :BACK_URL="BACK_URL" :curr_score="curr_score" :addScore="addScore"/>
    <br>
    <GameGrid :addScore="addScore" :GAME_SIZE="GAME_SIZE"/>
  </main>
</template>

<style scoped>
.center-block {
  height: 45vh;
  width: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}
</style>
