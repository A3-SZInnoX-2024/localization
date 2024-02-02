<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import axios from 'axios'
import { ref } from 'vue'

interface Color {
  color: string
  range: Array<[[number, number, number], [number, number, number]]>
}

interface Tag {
  tag: string
  position: [number, number]
}

const url = 'http://localhost:8000/'

const colors = ref<Color[]>([])
const tags = ref<Tag[]>([])

async function main() {
  const cls = await axios.get(url + 'colors')
  colors.value = cls.data
  const tgs = await axios.get(url + 'tags')
  console.log(tgs.data)
  tags.value = tgs.data
}

main()
</script>

<template>
  <header>
    <p class="title">A2 Configuration Control Panel</p>
  </header>

  <!-- <RouterView /> -->
</template>

<style scoped>
.title {
  padding-left: 4rem;
  padding-top: 2rem;
  font-size: 2rem;
}
</style>
