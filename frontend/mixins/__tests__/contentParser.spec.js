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
  test('parseImageContent', () => {
    const Component = {
      render() {},
      mixins: [ContentParser],
    }
    const wrapper = shallowMount(Component)
    expect(
      wrapper.vm.parseImageContent(
        '![My awesome cat](b1d1c9ef-c72f-4325-8c49-639278bf718d)'
      )
    ).toMatchObject({
      type: 'uuid-image',
      src: 'b1d1c9ef-c72f-4325-8c49-639278bf718d',
      alt: 'My awesome cat',
    })
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
          'Lerom ![desc](https://example.com/image.png) ipsum ![](eb286442-c745-4ee1-9f5c-0d9ac0a341f8) content',
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
        type: 'uuid-image',
        src: 'eb286442-c745-4ee1-9f5c-0d9ac0a341f8',
        alt: '',
      },
      {
        type: 'unparsed',
        text: ' content',
      },
    ])
  })
})
