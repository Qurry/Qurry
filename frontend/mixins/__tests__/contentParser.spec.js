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
})
