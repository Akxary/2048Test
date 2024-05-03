<script setup lang="ts">
import { getUserByName, type User } from './userFuncs';
</script>

<script lang="ts">
export default {
  data() {
    return {
      BACK_URL: "http://localhost:8005",
      MAX_VALUE: 2048,
      USER_NAME: 'test',
      CURR_SCORE: -1,
      USER_DATA: {id:1,name:"test", score:-1},
      MAX_RES_DATA: {id:-1, name:"", score: -1},
      grid: [
        [0, 0, 0, 0],
        [0, 2, 0, 0],
        [0, 0, 4, 0],
        [0, 0, 0, 0]
      ]
    }
  },
  methods: {
    async getUser() {
      this.USER_DATA = await fetch(`${this.BACK_URL}/user/name/${this.USER_NAME}`)
          .then(res => res.json())
      console.log(this.USER_DATA);
      console.log(this.USER_DATA.name);
      this.USER_NAME = this.USER_DATA.name;
    },

    async getMaxRes() {
      this.MAX_RES_DATA = await fetch(`${this.BACK_URL}/user/max-score/`)
      .then(res => res.json())
      console.log(this.MAX_RES_DATA);
    }
  },

  computed: {}
}
</script>

<template>
  <header>
    <!-- <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="You did it!" />
    </div> -->
  </header>

  <main>
    <button @click="getMaxRes">Получить рекорд</button>
    <br>
    <label for="name-inp">Введите имя пользователя</label>
    <br>
    <input v-model="USER_NAME" id="name-inp">
    <br>
    <button @click="getUser">Получить данные пользователя</button>
    <p>Имя пользователя: {{ USER_NAME }}</p>
    <p>Текущий счёт: {{ CURR_SCORE }}</p>
    <p>Максимальный счёт: {{ USER_DATA.score }}</p>
    <p>Рекорд {{ MAX_RES_DATA.score}} поставлен пользователем {{ MAX_RES_DATA.name}}</p>
    <div>
      <div v-for="(row, idx) in grid" :key="idx">
        <div v-for="(num, idx1) in row" :key="idx1" style="display: inline-flex; margin: 3px; padding: 3px;">
          <div v-if="num!=0" style="height: 25px; width: 25px; background-color: green;">{{ num }}</div>
          <div v-else style="height: 25px; width: 25px; background-color: aqua;"></div>
        </div>
      </div>
    </div>
    <!-- <TheWelcome /> -->
  </main>
</template>
<!-- ./userFuncs -->
