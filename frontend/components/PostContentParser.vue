<template>
  <div>
    <template v-for="(contentBlock, index) in contentBlocks">
      <template v-if="contentBlock.type === 'unparsed'">
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

    contentBlocks = this.parseContentBlocks(this.parseCode, contentBlocks, [
      'block',
      '```',
    ])
    contentBlocks = this.parseContentBlocks(this.parseCode, contentBlocks, [
      'inline',
      '`',
    ])
    return contentBlocks
  }

  parseContentBlocks(
    parseFunction: (contentBlock: ContentBlock, ...args: any) => ContentBlock[],
    contentBlocks: ContentBlock[],
    args: any[]
  ) {
    const newContentBlocks: ContentBlock[] = []
    for (let i = 0; i < contentBlocks.length; i++) {
      if (contentBlocks[i].type === 'unparsed') {
        const parsedContentBlocks = parseFunction(contentBlocks[i], ...args)
        newContentBlocks.push(...parsedContentBlocks)
      } else {
        newContentBlocks.push(contentBlocks[i])
      }
    }
    return newContentBlocks
  }

  parseCode(
    contentBlock: ContentBlock,
    mode: 'inline' | 'block',
    delimiter: string
  ) {
    const contentBlocks: ContentBlock[] = []
    const blockCodeRegex = new RegExp(
      '<[a-z]+>' + delimiter + '(?:[^`]|(?:(?<=\\\\)`))+(?<!\\\\)' + delimiter,
      'g'
    )
    const otherContentSegments = contentBlock.value.split(blockCodeRegex)
    const blockCodeSegments = contentBlock.value.match(blockCodeRegex)
    contentBlocks.push({
      type: 'unparsed',
      value: otherContentSegments[0],
    })
    if (blockCodeSegments) {
      for (let i = 0; i < blockCodeSegments.length; i++) {
        const lang = blockCodeSegments[i].match(/<[a-z]+>/)![0].slice(1, -1)
        contentBlocks.push({
          type: mode + '-code',
          lang,
          value: blockCodeSegments[i]
            .slice(lang.length + 2 + delimiter.length, -1 * delimiter.length)
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
}
</script>

<style scoped></style>
