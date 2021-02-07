<template>
  <v-row>
    <v-col>
      <v-md-editor
        :value="value"
        height="500px"
        left-toolbar="undo redo | h bold italic strikethrough quote ul ol table hr link image code latex"
        :toolbar="toolbar"
        @input="$emit('input', $event)"
      ></v-md-editor>
    </v-col>
  </v-row>
</template>

<script>
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { code, image } from '@kangc/v-md-editor/lib/utils/constants/command'

@Component({ auth: false })
export default class PostBodyInput extends Vue {
  @Prop()
  value

  toolbar = {
    latex: {
      title: 'Latex',
      icon: 'v-md-icon-tip',
      menus: [
        {
          name: 'inline-latex',
          text: 'Inline Latex',
          action(editor) {
            editor.insert(function (selected) {
              const delimiter = '$'
              const placeholder = 'a+b'
              const content = selected || placeholder

              return {
                text: `${delimiter}${content}${delimiter}`,
                selected: content,
              }
            })
          },
        },
        {
          name: 'block-latex',
          text: 'Block Latex',
          action(editor) {
            editor.insert(function (selected) {
              const delimiter = '$$'
              const placeholder = 'a+b'
              const content = selected || placeholder

              return {
                text: `${delimiter}${content}${delimiter}`,
                selected: content,
              }
            })
          },
        },
      ],
    },
    code: {
      title: 'Code',
      icon: 'v-md-icon-code',
      menus: [
        {
          name: 'inline-code',
          text: 'Inline Code',
          action(editor) {
            editor.insert(function (selected) {
              const delimiter = '`'
              const placeholder = 'code'
              const content = selected || placeholder

              return {
                text: `${delimiter}${content}${delimiter}`,
                selected: content,
              }
            })
          },
        },
        {
          name: 'block-code',
          text: 'Block Code',
          action(editor) {
            editor.execCommand(code)
          },
        },
      ],
    },
    image: {
      title: 'Image',
      icon: 'v-md-icon-img',
      menus: [
        {
          name: 'image-link',
          text: 'Image Link',
          action(editor) {
            editor.execCommand(image)
          },
        },
        {
          name: 'image-with-size',
          text: 'Image with size',
          action(editor) {
            editor.execCommand(image, { width: 'auto', height: 'auto' })
          },
        },
      ],
    },
  }
}
</script>

<style scoped></style>
