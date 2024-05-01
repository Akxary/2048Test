<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue'
import TheWelcome from './components/TheWelcome.vue'
import { getUserByName, User } from './userFuncs';
</script>

<script lang="ts">
export default {
  data() {
    return {
      MAX_VALUE: 2048,
      USER_NAME: 'test',
      USER_DATA: {id:1,name:"test", score:-1},
      grid: [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
      ]
    }
  },
  methods: {
    async getUser() {
      this.USER_DATA = await getUserByName(this.USER_NAME);
      console.log(this.USER_DATA);
      console.log(this.USER_DATA.name);
      this.USER_NAME = this.USER_DATA.name;
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
    
    <label for="name-inp">Введите имя пользователя</label>
    <br>
    <input v-model="USER_NAME" id="name-inp">
    <br>
    <button @click="getUser">Get user</button>
    <p>Current name is: {{ USER_NAME }}</p>
    <p>Current score is: {{ USER_DATA.score }}</p>

    <div>
      <div v-for="(row, idx) in grid" :key="idx">
        <div v-for="(num, idx1) in row" :key="idx1" style="display: inline-flex; margin: 3px; padding: 3px;">
          <div v-if="num!=0">{{ num }}</div>
          <div v-else style="height: 25px; width: 25px; background-color: aqua;"></div>
        </div>
      </div>
    </div>
    <!-- <TheWelcome /> -->
  </main>
</template>
<!-- ./userFuncs -->
