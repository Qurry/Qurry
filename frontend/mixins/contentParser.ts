import { Component, Vue } from 'nuxt-property-decorator'

export interface Content {
  type: string
}

interface UnparsedContent extends Content {
  type: 'unparsed'
  text: string
}

interface CodeContent extends Content {
  type: 'inline-code' | 'block-code'
  text: string
  language: string
}

interface LatexContent extends Content {
  type: 'inline-latex' | 'block-latex'
  text: string
}

interface ImageContent extends Content {
  type: 'uuid-image' | 'url-image'
  src: string
  alt: string
}

interface TextContent extends Content {
  type: 'text'
  text: string
}

@Component
export class ContentParser extends Vue {
  parseContents(rawText: string, mode: string) {
    let contents: Content[] = []

    contents.push({
      type: 'unparsed',
      text: rawText,
    } as UnparsedContent)

    if (mode === 'body') {
      contents = this.parseContentsWithFunction(
        contents,
        this.parseBlockCodeContents
      )
      contents = this.parseContentsWithFunction(
        contents,
        this.parseInlineCodeContents
      )
      contents = this.parseContentsWithFunction(
        contents,
        this.parseImageContents
      )
    }

    return contents
  }

  parseContentsWithFunction(
    unparsedContents: Content[],
    parseFunction: (unparsedContent: UnparsedContent) => Content[]
  ) {
    const parsedContents: Content[] = []
    for (const unparsedContent of unparsedContents) {
      if (unparsedContent.type === 'unparsed') {
        parsedContents.push(
          ...parseFunction(unparsedContent as UnparsedContent)
        )
      } else {
        parsedContents.push(unparsedContent)
      }
    }
    return parsedContents
  }

  parseInlineCodeContents(
    unparsedContent: UnparsedContent
  ): (CodeContent | UnparsedContent)[] {
    return this.parseCodeContents(unparsedContent, 'inline', '`')
  }

  parseBlockCodeContents(
    unparsedContent: UnparsedContent
  ): (CodeContent | UnparsedContent)[] {
    return this.parseCodeContents(unparsedContent, 'block', '```')
  }

  parseCodeContents(
    unparsedContent: UnparsedContent,
    mode: 'inline' | 'block',
    delimiter: string
  ): (CodeContent | UnparsedContent)[] {
    const parsedContents: (CodeContent | UnparsedContent)[] = []
    const codeRegex = new RegExp(
      '<[a-z0-9-]+>' +
        delimiter +
        '(?:[^`]|(?:(?<=\\\\)`))+(?<!\\\\)' +
        delimiter,
      'g'
    )
    const unparsedSegments = unparsedContent.text.split(codeRegex)
    const codeSegments = unparsedContent.text.match(codeRegex)
    parsedContents.push(this.parseUnparsedContent(unparsedSegments[0]))
    if (codeSegments) {
      for (let i = 0; i < codeSegments.length; i++) {
        parsedContents.push(
          this.parseCodeContent(codeSegments[i], mode, delimiter)
        )
        parsedContents.push(this.parseUnparsedContent(unparsedSegments[i + 1]))
      }
    }
    return parsedContents
  }

  parseCodeContent(
    segment: string,
    mode: 'inline' | 'block',
    delimiter: string
  ): CodeContent {
    const language = segment.match(/<[a-z0-9-]+>/)![0].slice(1, -1)
    return {
      type: mode + '-code',
      language,
      text: segment
        .slice(language.length + 2 + delimiter.length, -1 * delimiter.length)
        .replace('\\`', '`'),
    } as CodeContent
  }

  parseImageContents(unparsedContent: UnparsedContent) {
    const parsedContents: (ImageContent | UnparsedContent)[] = []
    const imageRegex = /!\[[^\]]*\]\([^)]*\)/g
    const unparsedSegments = unparsedContent.text.split(imageRegex)
    const imageSegments = unparsedContent.text.match(imageRegex)
    parsedContents.push(this.parseUnparsedContent(unparsedSegments[0]))
    if (imageSegments) {
      for (let i = 0; i < imageSegments.length; i++) {
        parsedContents.push(this.parseImageContent(imageSegments[i]))
        parsedContents.push(this.parseUnparsedContent(unparsedSegments[i + 1]))
      }
    }
    return parsedContents
  }

  parseImageContent(segment: string): ImageContent {
    const uuidRegex = /[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}/
    const altText = segment.slice(2).split(']')[0]
    const source = segment.slice(0, -1).split('](')[1]
    return {
      type: uuidRegex.test(source) ? 'uuid-image' : 'url-image',
      src: source,
      alt: altText,
    } as ImageContent
  }

  parseUnparsedContent(segment: string): UnparsedContent {
    return {
      type: 'unparsed',
      text: segment,
    } as UnparsedContent
  }
}
