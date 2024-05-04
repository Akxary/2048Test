<script lang="ts">
import UserInfo from "./UserInfo.vue";
export default {
  components: {UserInfo},
  props: {
    BACK_URL: {
      type: String,
      required: true,
    },
    curr_score: {
      type: Number,
      required: true,
      default: 0,
    },
    addScore: {
      type: Function,
      required: true,
    }
  },
  data() {
    return {
      user_name: 'test',
      user_data: {id: 1, name: "test", score: -1},
      max_res_data: {id: -1, name: "", score: -1},
      showPopupFlg: false,
      authFlg: false,
      testValue: "1",
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
    },

    showPopup() {
      if (this.showPopupFlg)
        this.showPopupFlg = false;
      this.showPopupFlg = true;
    },

    formatThousands(value: number):string {
      let res:string = "";
      let num:number = Math.floor(value);
      let subNum:number;
      let subStr:string;
      while (num>0) {
        subNum=num%1000;
        subStr = `${subNum}`;
        while (subStr.length<3) {
          subStr = "0"+subStr;
        }
        res = subStr+ " " + res;
        num = Math.floor(num/1000);
      }
      return res.trim();
    }
  }
}
</script>

<template>
  <div class="ramka">
    <button @click="addScore(1233)">Добавить счёт</button>
    <button v-if="authFlg" @click="showPopup">{{ user_name }}</button>
    <button v-else @click="showPopup">Войти</button>
    <UserInfo v-if="showPopupFlg"/>
    <button @click="getMaxRes">Получить рекорд</button>
    <br>
    <label for="name-inp">Введите имя пользователя</label>
    <br>
    <input v-model="user_name" id="name-inp">
    <br>
    <button @click="getUser">Получить данные пользователя</button>
    <p>Имя пользователя: {{ user_name }}</p>
    <p>Текущий счёт: {{ formatThousands(curr_score) }}</p>
    <p>Максимальный счёт: {{ user_data.score }}</p>
    <p>Рекорд {{ formatThousands(max_res_data.score) }} поставлен пользователем {{ max_res_data.name }}</p>
  </div>
</template>

<style scoped>
.ramka {
  width: 44vh;
  border: .3vh solid coral;
  border-radius: 1vh;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  flex-direction: column;
}



</style>