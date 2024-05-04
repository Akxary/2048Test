<script lang="ts">
import handleTouches from './handleTouches';
import handlePresses from "./handlePresses";
export default {
  props: {

    setScore: {
      type: Function,
      required: true
    },
    curr_score: {
      type: Number,
      required: true,
    },
    GAME_SIZE: {
      type: Number,
      required: true,
    }
  },
  data() {
    return {
      grid: [[0]],
      addToScore: 0,
      showPopupFlg: false,
    }
  },
  created() {
    this.grid = [...Array(this.GAME_SIZE)].map((j, idx0) => [...Array(this.GAME_SIZE)].map((i, idx) => 2 * Math.pow(2, idx0+idx)));
      },
  mounted() {
      handleTouches("game-container");
      handlePresses("game-container");
  },
  methods: {
    moveByKey(key: string) {
      console.log("key pressed: " + key);
      console.log("grid before transform:");
      console.log(this.grid);
      // обнуление очков в накопителе
      this.addToScore = 0;
      let newGrid: Array<Array<number>>;
      switch (key) {
        case "ArrowUp":
          newGrid = this.moveUp();
          break;
        case "ArrowDown":
          newGrid = this.moveDown();
          break;
        case "ArrowRight":
          newGrid = this.moveRight();
          break;
        case "ArrowLeft":
          newGrid = this.moveLeft();
          break;
        default:
          return;
      }
      if (this.arrayEquals(newGrid, this.grid)) {

        return;
      }
      // начисление очков
      this.setScore(this.curr_score + this.addToScore);

      newGrid = this.createNewElement(newGrid);
      this.grid = newGrid;
      // проверка жизнеспособности нового положения игры
      if (this.countZeros(this.grid) == 0) {
        if (
            this.arrayEquals(this.grid, this.moveRight())
            // && this.arrayEquals(this.grid, this.moveLeft())
            // && this.arrayEquals(this.grid, this.moveUp())
            // && this.arrayEquals(this.grid, this.moveDown())
        ) {
          alert(`Вы проиграли. Ваш счёт: ${this.curr_score}`);
          // this.newGame();
        }
      }
    },

    arrayEquals(left: Array<Array<number>>, right: Array<Array<number>>): boolean {
      for (let i = 0; i < this.GAME_SIZE; i++) {
        for (let j = 0; j < this.GAME_SIZE; j++) {
          if (left[i][j] !== right[i][j]) {
            return false;
          }
        }
      }
      return true;
    },

    countZeros: function (grid: Array<Array<number>>): number {
      let count = 0;
      let row: Array<number>;
      let i: number;
      for (row of grid) {
        for (i of row) {
          if (i == 0) count++;
        }
      }
      return count;
    },

    createNewElement(newGrid: Array<Array<number>>): Array<Array<number>> {
      const newVal: number = Math.random() <= 0.1 ? 4 : 2; // выпадает 4 с вероятностью 10%


      let zeroIdxs: Array<number> = [];

      for (let i1: number = 0; i1 < this.GAME_SIZE; i1++) {
        for (let j1: number = 0; j1 < this.GAME_SIZE; j1++) {
          if (newGrid[i1][j1] == 0) {
            zeroIdxs.push(i1 * this.GAME_SIZE + j1);
          }
        }
      }
      let newIdx: number = zeroIdxs[Math.floor(Math.random() * zeroIdxs.length)];
      let i: number = Math.floor(newIdx / this.GAME_SIZE);
      let j: number = newIdx % this.GAME_SIZE;
      // краш при одной свободной ячейке
      // do {
      //   i = Math.floor(Math.random()*(this.GAME_SIZE-1));
      //   j = Math.floor(Math.random()*(this.GAME_SIZE-1));
      //   console.log("i = "+i);
      //   console.log("j = "+j);
      // } while (newGrid[i][j]!=0)

      newGrid[i][j] = newVal;

      return newGrid;
    },

    processRow(row: Array<number>): Array<number> {
      let el: number;
      let newRow: Array<number> = [];
      for (el of row) {
        if (el != 0)
          newRow.push(el);
      }
      // соединяем элементы, если это возможно
      for (let i: number = newRow.length - 1; i >= 1; i--) {
        if (newRow[i] == newRow[i - 1]) {
          newRow[i] = 2 * newRow[i];
          // добавляем очки после соединения
          this.addToScore += newRow[i];
          // удаляем предыдущий элемент, с которым соединились
          newRow.splice(i - 1, 1);
          i--;
        }
      }
      // добавляем нулей
      const rowLength = newRow.length;
      for (let i: number = 0; i < this.GAME_SIZE - rowLength; i++) {
        newRow.unshift(0);
      }
      return newRow;
    },

    transpose(oldGrid: Array<Array<number>>): Array<Array<number>> {
      // создаём пустой массив с нулями
      let newGrid: Array<Array<number>> = [...Array(this.GAME_SIZE)].map(() => [...Array(this.GAME_SIZE)].map(() => 0));
      for (let i: number = 0; i < this.GAME_SIZE; i++) {
        for (let j: number = 0; j < this.GAME_SIZE; j++) {
          newGrid[i][j] = oldGrid[j][i];
        }
      }
      return newGrid;
    },

    reorder(oldGrid: Array<Array<number>>): Array<Array<number>> {
      let newGrid: Array<Array<number>> = [...Array(this.GAME_SIZE)].map(() => [...Array(this.GAME_SIZE)].map(() => 0));
      for (let i: number = 0; i < this.GAME_SIZE; i++) {
        for (let j: number = 0; j < this.GAME_SIZE; j++) {
          newGrid[i][j] = oldGrid[i][this.GAME_SIZE - j - 1];
        }
      }
      return newGrid;
    },

    baseMove(moveGrid: Array<Array<number>>): Array<Array<number>> {
      let newGrid: Array<Array<number>> = [];
      let row: number[];
      for (row of moveGrid) {
        newGrid.push(this.processRow(row));
      }
      return newGrid;
    },

    moveRight(): Array<Array<number>> {
      return this.baseMove(this.grid);
    },

    moveLeft(): Array<Array<number>> {
      let trGrid: Array<Array<number>> = this.reorder(this.grid);
      let newGrid: Array<Array<number>> = this.baseMove(trGrid);
      return this.reorder(newGrid);
    },

    moveDown(): Array<Array<number>> {
      let trGrid: Array<Array<number>> = this.transpose(this.grid);
      let newGrid: Array<Array<number>> = this.baseMove(trGrid);
      return this.transpose(newGrid);
    },

    moveUp(): Array<Array<number>> {
      let trGrid: Array<Array<number>> = this.reorder(this.transpose(this.grid));
      let newGrid: Array<Array<number>> = this.baseMove(trGrid);
      return this.transpose(this.reorder(newGrid));
    },

    setFocus() {
      this.$refs.gamegrid.focus();
      // console.log(this.$refs.gamegrid);
    },

    newGame() {
      this.setScore(0);
      this.grid = [...Array(this.GAME_SIZE)].map(() => [...Array(this.GAME_SIZE)].map(() => 0));
      this.grid = this.createNewElement(this.createNewElement(this.grid));
      // this.setFocus();
    }
  }
}
</script>

<template>
  <div class="line-div">
    <button @click="newGame">Новая игра</button>
<!--    <input ref="gamegrid" @keydown="(event)=>{console.log(event);moveByKey(event.key)}" type="text" class="micro-input">-->
  </div>
<!--  @keydown="(event)=>{console.log(event);moveByKey(event.key)}"-->
<!--@click="setFocus"-->
  <div id="game-container"  @keydown="(event)=>{console.log(event);moveByKey(event.key)}"  class="grid-style">
    <div v-for="(row, idx) in grid" :key="idx" class="line-div">
      <div v-for="(num, idx1) in row" :key="idx1" style="padding: 3px">
        <div v-if="num!=0" :class="num<2048?`cell-${num}`:`cell-2048`" class="cell-no-0 base-cell">{{ num }}</div>
        <div v-else class="cell-0 base-cell">-</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
input, input:focus {
  font-size: 0;
  width: 0;
  height: 0;
  border: none;
  background: transparent;
  color: transparent;
}


.grid-style {
  border: coral 5px solid;
  border-radius: 5px;
  background-color: aliceblue;
  display: flex;
  flex-direction: column;
}

.line-div {
  display: inline-flex;
  padding: 2px;
}

.cell-no-0 {
  font-size: 3vh;

}

.cell-0 {
  background-color: lightgrey;
  font-size: 0;
}

.base-cell {
  height: 10vh;
  width: 10vh;
  border-radius: 1vh;
  display: flex;
  align-content: center;
  justify-content: center;
  align-items: center;
}

</style>