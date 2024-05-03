<script lang="ts">
export default {
  props: {
    BACK_URL: {
      type: String,
      required: true,
    },
    curr_score: {}
  },
  data() {
    return {
      user_name: 'test',
      user_data: {id: 1, name: "test", score: -1},
      max_res_data: {id: -1, name: "", score: -1},
    }
  },
  methods: {
    async getUser() {
      this.user_data = await fetch(`${this.BACK_URL}/user/name/${this.user_name}`)
          .then(res => res.json())
      // console.log(this.user_data);
      // console.log(this.user_data.name);
      // this.user_name = this.user_data.name;
    },

    async getMaxRes() {
      this.max_res_data = await fetch(`${this.BACK_URL}/user/max-score/`)
          .then(res => res.json())
      // console.log(this.max_res_data);
    }
  }
}
</script>

<template>
  <div class="ramka">
    <button @click="getMaxRes">Получить рекорд</button>
    <br>
    <label for="name-inp">Введите имя пользователя</label>
    <br>
    <input v-model="user_name" id="name-inp">
    <br>
    <button @click="getUser">Получить данные пользователя</button>
    <p>Имя пользователя: {{ user_name }}</p>
    <p>Текущий счёт: {{ curr_score }}</p>
    <p>Максимальный счёт: {{ user_data.score }}</p>
    <p>Рекорд {{ max_res_data.score }} поставлен пользователем {{ max_res_data.name }}</p>
  </div>
</template>

<style scoped>
.ramka {
  border: 1px solid red;
  border-radius: 5px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}
</style>