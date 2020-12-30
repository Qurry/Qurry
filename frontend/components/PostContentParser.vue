<template>
  <div>
    <template v-for="(contentBlock, index) in contentBlocks">
      <template v-if="contentBlock.type === 'text'">
        <span :key="index">{{ contentBlock.value }} </span>
        <!-- <span :key="index" v-html="$md.render(contentBlock.value)"></span> -->
      </template>
      <template v-else-if="contentBlock.type === 'bold-text'">
        <strong :key="index">{{ contentBlock.value }} </strong>
      </template>
      <template v-else-if="contentBlock.type === 'block-code'">
        <pre :key="index"><code :class="'lang-' + contentBlock.lang">{{
          contentBlock.value
        }}</code></pre>
      </template>
      <template v-else-if="contentBlock.type === 'inline-code'">
        <code :key="index" :class="'lang-' + contentBlock.lang">{{
          contentBlock.value
        }}</code>
      </template>
    </template>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import Prism from 'prismjs'

interface ContentBlock {
  type: string
  value: string
  lang?: string
}

@Component
export default class PostContentParser extends Vue {
  @Prop()
  content!: string
  // content =
  //   'This is some css <code class="lang-css">a: {color: red} and some python code <python>`print(ab\\`c)` Awesome'

  contentBlocks: ContentBlock[] = []

  created() {
    this.contentBlocks = this.parseContent(this.content)
  }

  mounted() {
    Prism.highlightAll()
  }

  parseContent(content: string) {
    let contentBlocks: ContentBlock[] = []
    contentBlocks.push({ type: 'unparsed', value: content })

    contentBlocks = this.parseContentBlocks(contentBlocks, this.parseBlockCode)
    contentBlocks = this.parseContentBlocks(contentBlocks, this.parseInlineCode)
    return contentBlocks
  }

  parseContentBlocks(
    contentBlocks: ContentBlock[],
    parseFunction: (contentBlock: ContentBlock) => ContentBlock[]
  ) {
    const newContentBlocks: ContentBlock[] = []
    for (let i = 0; i < contentBlocks.length; i++) {
      if (contentBlocks[i].type === 'unparsed') {
        const parsedContentBlocks = parseFunction(contentBlocks[i])
        newContentBlocks.push(...parsedContentBlocks)
      } else {
        newContentBlocks.push(contentBlocks[i])
      }
    }
    return newContentBlocks
  }

  parseBlockCode(contentBlock: ContentBlock) {
    const contentBlocks: ContentBlock[] = []
    const blockCodeRegex = /<[a-z]+>```(?:[^`]|(?:(?<=\\)`))+```/g
    const otherContentSegments = contentBlock.value.split(blockCodeRegex)
    const blockCodeSegments = contentBlock.value.match(blockCodeRegex)
    contentBlocks.push({
      type: 'unparsed',
      value: otherContentSegments[0],
    })
    if (blockCodeSegments) {
      for (let i = 0; i < blockCodeSegments.length; i++) {
        contentBlocks.push({
          type: 'block-code',
          lang: blockCodeSegments[i].match(/<[a-z]+>/)![0].slice(1, -1),
          value: blockCodeSegments[i]
            .split(/<[a-z]+>/)[1]
            .slice(3, -3)
            .replace('\\`', '`'),
        })
        contentBlocks.push({
          type: 'unparsed',
          value: otherContentSegments[i + 1],
        })
      }
    }
    return contentBlocks
  }

  parseInlineCode(contentBlock: ContentBlock) {
    const contentBlocks: ContentBlock[] = []
    const inlineCodeRegex = /<[a-z]+>`(?:[^`]|(?:(?<=\\)`))+(?<!\\)`/g
    const otherContentSegments = contentBlock.value.split(inlineCodeRegex)
    const inlineCodeSegments = contentBlock.value.match(inlineCodeRegex)
    contentBlocks.push({
      type: 'text',
      value: otherContentSegments[0],
    })
    if (inlineCodeSegments) {
      for (let i = 0; i < inlineCodeSegments.length; i++) {
        contentBlocks.push({
          type: 'inline-code',
          lang: inlineCodeSegments[i].match(/<[a-z]+>/)![0].slice(1, -1),
          value: inlineCodeSegments[i]
            .split(/<[a-z]+>/)[1]
            .slice(1, -1)
            .replace('\\`', '`'),
        })
        contentBlocks.push({
          type: 'text',
          value: otherContentSegments[i + 1],
        })
      }
    }
    return contentBlocks
  }
}
</script>

<style scoped></style>
