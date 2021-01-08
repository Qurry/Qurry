<template>
  <div>
    <template v-for="(content, index) in contents">
      <template v-if="content.type === 'unparsed'">
        <MathJaxParser :key="index" :content="content.text" />
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
      <!-- <template v-else-if="content.type === 'url-image'">
        <img :key="index" :src="content.text" alt="alt-image" width="200px" />
      </template> -->
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
