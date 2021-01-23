import { shallowMount } from '@vue/test-utils'
import { ContentParser } from '@/mixins/contentParser'

describe('ContentParser', () => {
  test('parseUnparsedContent', () => {
    const Component = {
      render() {},
      mixins: [ContentParser],
    }
    const wrapper = shallowMount(Component)
    expect(wrapper.vm.parseUnparsedContent('some content')).toMatchObject({
      type: 'unparsed',
      text: 'some content',
    })
    expect(wrapper.vm.parseUnparsedContent('')).toMatchObject({
      type: 'unparsed',
      text: '',
    })
  })
  test('parseCodeContent', () => {
    const Component = {
      render() {},
      mixins: [ContentParser],
    }
    const wrapper = shallowMount(Component)
    expect(
      wrapper.vm.parseCodeContent('<python>`print(a)`', 'inline', '`')
    ).toMatchObject({
      type: 'inline-code',
      language: 'python',
      text: 'print(a)',
    })
    expect(
      wrapper.vm.parseCodeContent('<html>`<p>pri\\`nt</p>`', 'inline', '`')
    ).toMatchObject({
      type: 'inline-code',
      language: 'html',
      text: '<p>pri`nt</p>',
    })
    expect(
      wrapper.vm.parseCodeContent(
        '<jin-ja2>```{% raw %}His name is\\` {{ name }}{% endraw %}```',
        'block',
        '```'
      )
    ).toMatchObject({
      type: 'block-code',
      language: 'jin-ja2',
      text: '{% raw %}His name is` {{ name }}{% endraw %}',
    })
  })
  test('parseCodeContents', () => {
    const Component = {
      render() {},
      mixins: [ContentParser],
    }
    const wrapper = shallowMount(Component)
    expect(
      wrapper.vm.parseCodeContents(
        { type: 'unparsed', text: 'some content' },
        'inline',
        '`'
      )
    ).toMatchObject([
      {
        type: 'unparsed',
        text: 'some content',
      },
    ])
    expect(
      wrapper.vm.parseCodeContents(
        { type: 'unparsed', text: 'some <python>`print(a)` content' },
        'inline',
        '`'
      )
    ).toMatchObject([
      {
        type: 'unparsed',
        text: 'some ',
      },
      {
        type: 'inline-code',
        language: 'python',
        text: 'print(a)',
      },
      {
        type: 'unparsed',
        text: ' content',
      },
    ])
  })
  test('parseLatexContents', () => {
    const Component = {
      render() {},
      mixins: [ContentParser],
    }
    const wrapper = shallowMount(Component)
    expect(
      wrapper.vm.parseLatexContents(
        { type: 'unparsed', text: 'some content' },
        'inline',
        '$'
      )
    ).toMatchObject([
      {
        type: 'unparsed',
        text: 'some content',
      },
    ])
    expect(
      wrapper.vm.parseLatexContents(
        {
          type: 'unparsed',
          text: 'let $a\\$bc$ be \\$and $$\\sum_a$$ not $$34\\$$$',
        },
        'block',
        '$$'
      )
    ).toMatchObject([
      {
        type: 'unparsed',
        text: 'let $a\\$bc$ be \\$and ',
      },
      {
        type: 'block-latex',
        text: '\\sum_a',
      },
      {
        type: 'unparsed',
        text: ' not ',
      },
      {
        type: 'block-latex',
        text: '34\\$',
      },
      {
        type: 'unparsed',
        text: '',
      },
    ])
  })
  test('parseImageContent', () => {
    const Component = {
      render() {},
      mixins: [ContentParser],
    }
    const wrapper = shallowMount(Component)
    expect(wrapper.vm.parseImageContent('![My awesome cat](56)')).toMatchObject(
      {
        type: 'id-image',
        src: '56',
        alt: 'My awesome cat',
      }
    )
    expect(
      wrapper.vm.parseImageContent(
        '![Image of Yaktocat](https://octodex.github.com/images/yaktocat.png)'
      )
    ).toMatchObject({
      type: 'url-image',
      src: 'https://octodex.github.com/images/yaktocat.png',
      alt: 'Image of Yaktocat',
    })
  })
  test('parseImageContents', () => {
    const Component = {
      render() {},
      mixins: [ContentParser],
    }
    const wrapper = shallowMount(Component)
    expect(
      wrapper.vm.parseImageContents({ type: 'unparsed', text: 'some content' })
    ).toMatchObject([
      {
        type: 'unparsed',
        text: 'some content',
      },
    ])
    expect(
      wrapper.vm.parseImageContents({
        type: 'unparsed',
        text:
          'Lerom ![desc](https://example.com/image.png) ipsum ![](4) content',
      })
    ).toMatchObject([
      {
        type: 'unparsed',
        text: 'Lerom ',
      },
      {
        type: 'url-image',
        src: 'https://example.com/image.png',
        alt: 'desc',
      },
      {
        type: 'unparsed',
        text: ' ipsum ',
      },
      {
        type: 'id-image',
        src: '4',
        alt: '',
      },
      {
        type: 'unparsed',
        text: ' content',
      },
    ])
  })
})
