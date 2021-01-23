<template>
  <div>
    <template v-for="(content, index) in contents">
      <template v-if="content.type === 'unparsed'">
        <span :key="index" style="white-space: pre">{{ content.text }}</span>
      </template>
      <template v-else-if="content.type === 'block-code'">
        <pre :key="index"><code :class="'lang-' + content.language">{{
          content.text
        }}</code></pre>
      </template>
      <template v-else-if="content.type === 'inline-code'">
        <code :key="index" :class="'lang-' + content.language">{{
          content.text
        }}</code>
      </template>
      <template v-else-if="content.type === 'block-latex'">
        <katex-element
          :key="index"
          :expression="content.text"
          :display-mode="true"
        />
      </template>
      <template v-else-if="content.type === 'inline-latex'">
        <katex-element :key="index" :expression="content.text" />
      </template>
      <template v-else-if="content.type === 'url-image'">
        <img
          :key="index"
          :src="content.src"
          :alt="'<<< NO IMAGE FOUND WITH URL=' + content.src + ' >>>'"
        />
      </template>
      <template v-else-if="content.type === 'id-image'">
        <img
          :key="index"
          :src="imageUrls[parseInt(content.src) - 1]"
          :alt="'<<< NO IMAGE FOUND WITH ID=' + content.src + ' >>>'"
        />
      </template>
    </template>
  </div>
</template>

<script lang="ts">
import { Component, Prop, mixins } from 'nuxt-property-decorator'
import Prism from 'prismjs'
import { ContentParser, Content } from '../mixins/contentParser'

@Component
export default class PostContentParser extends mixins(ContentParser) {
  @Prop()
  content!: string

  @Prop()
  imageUrls!: string[]

  @Prop()
  mode!: string

  contents: Content[] = []

  created() {
    this.contents = this.parseContents(this.content, this.mode)
  }

  mounted() {
    Prism.highlightAll()
  }
}
</script>

<style scoped></style>
