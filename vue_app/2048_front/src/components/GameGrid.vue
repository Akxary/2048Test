<script lang="ts">

export default {

  props: {

    addScore: {
      type: Function,
      required: true
    },
    GAME_SIZE: {
      type: Number,
      required: true,
    }
  },
  data() {
    return {
      grid:[[0]],
    }
  },
  created() {
      this.grid = [... Array(this.GAME_SIZE)].map(()=>[...Array(this.GAME_SIZE)].map(()=>0))
  },
  methods: {
    moveByKey(key: string) {
      // console.log(key);
      let newGrid: Array<Array<number>>;
      switch (key) {
        case "ArrowUp":
          newGrid = this.moveUp();
          break;
        case "ArrowDown":
          newGrid = this.moveDown();
          break;
        case "ArrowRight":
          newGrid = this.moveLeft();
          break;
        case "ArrowLeft":
          newGrid = this.moveRight();
          break;
        default:
          return;
      }
      if (newGrid==this.grid) {alert("end game")}
      newGrid = this.createNewElement(newGrid);
      this.grid = newGrid;
    },

    createNewElement(newGrid: Array<Array<number>>): Array<Array<number>> {
      const newVal: number = Math.random()<=0.1?4:2; // выпадает 4 с вероятностью 10%

      let i:number;
      let j:number;

      do {
        i = Math.floor(Math.random()*(this.GAME_SIZE-1));
        j = Math.floor(Math.random()*(this.GAME_SIZE-1));
      } while (this.grid[i][j]!=0)

      newGrid[i][j] = newVal;

      return newGrid;
    },

    processRow(row: Array<number>): Array<number> {
      let el:number;
      let newRow:Array<number> = [];
      for (el of row) {
        if (el!=0)
          newRow.push(el);
      }
      // соединяем элементы, если это возможно
      for (let i:number = newRow.length-1; i >=1; i--) {
        if (newRow[i]==newRow[i-1]) {
          newRow[i] = 2*newRow[i];
          // добавляем очки после соединения
          this.addScore(newRow[i]);
          // удаляем предыдущий элемент, с которым соединились
          newRow.splice(i-1, 1);
        }
      }
      // добавляем нулей
      for (let i:number = 0; i <newRow.length-1 - this.GAME_SIZE; i++) {
           newRow.unshift(0);
      }
      return newRow;
    },

    transpose(oldGrid:Array<Array<number>>): Array<Array<number>> {
      // создаём пустой массив с нулями
      let newGrid: Array<Array<number>> = [... Array(this.GAME_SIZE)].map(()=>[...Array(this.GAME_SIZE)].map(()=>0));
      for (let i:number = 0; i <this.GAME_SIZE-1; i++) {
        for (let j:number=0; j<this.GAME_SIZE-1; j++) {
          newGrid[i][j] = oldGrid[j][i];
        }
      }
      return newGrid;
    },

    reorder(oldGrid:Array<Array<number>>): Array<Array<number>> {
      let newGrid: Array<Array<number>> = [... Array(this.GAME_SIZE)].map(()=>[...Array(this.GAME_SIZE)].map(()=>0));
      for (let i:number = 0; i <this.GAME_SIZE-1; i++) {
        for (let j: number = 0; j < this.GAME_SIZE - 1; j++) {
          newGrid[i][j] = oldGrid[i][this.GAME_SIZE-j-1];
        }
      }
      return newGrid;
    },

    baseMove(moveGrid: Array<Array<number>>): Array<Array<number>> {
      let newGrid: Array<Array<number>> = [];
      let row:number[];
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
      let newGrid:Array<Array<number>> = this.baseMove(trGrid);
      return this.reorder(newGrid);
    },

    moveDown(): Array<Array<number>> {
      let trGrid: Array<Array<number>> = this.transpose(this.grid);
      let newGrid:Array<Array<number>> = this.baseMove(trGrid);
      return this.transpose(newGrid);
    },

    moveUp(): Array<Array<number>> {
      let trGrid: Array<Array<number>> = this.reorder(this.transpose(this.grid));
      let newGrid:Array<Array<number>> = this.baseMove(trGrid);
      return this.transpose(this.reorder(newGrid));
    },

    setFocus() {
      this.$refs.gamegrid.focus();
      // console.log(this.$refs.gamegrid);
    }
  }
}
</script>

<template>
  <div class="line-div">
    <button @click="setFocus">Начать</button>
    <input ref="gamegrid" @keydown="(event)=>moveByKey(event.key)" type="text" class="micro-input">
  </div>

  <div @click="setFocus" class="grid-style">
    <div v-for="(row, idx) in grid" :key="idx">
      <div v-for="(num, idx1) in row" :key="idx1" class="line-div">
        <div v-if="num!=0" class="base-cell not-base-cell"><p>{{ num }}</p></div>
        <div v-else class="base-cell"><p>-</p></div>
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
}

.line-div {
  display: inline-flex;
  margin: 3px;
  padding: 3px;
}

.not-base-cell {
  background-color: green;
}

.base-cell {
  height: 10vh;
  width: 10vh;
  background-color: lightgrey;
  border-radius: 1vh;
}

</style>