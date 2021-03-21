<template>
  <v-row>
    <v-col>
      <v-md-editor
        :value="value"
        height="500px"
        left-toolbar="undo redo | h bold italic strikethrough quote ul ol table hr link image code latex"
        :toolbar="toolbar"
        :disabled-menus="[]"
        @upload-image="handleUploadImage"
        @input="$emit('input', $event)"
      ></v-md-editor>
    </v-col>
  </v-row>
</template>

<script>
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { code, image } from '@kangc/v-md-editor/lib/utils/constants/command'
import { filesFilter } from '@kangc/v-md-editor/lib/utils/file'

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
          name: 'upload-image',
          text: 'Upload Image',
          action(editor) {
            editor.uploadConfig = editor.uploadImgConfig
            editor.$nextTick(async () => {
              const event = await editor.$refs.uploadFile.upload()
              const files = filesFilter(
                event.target.files,
                editor.uploadImgConfig
              )

              editor.emitUploadImage(event, files)
            })
          },
        },
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

  handleUploadImage(_event, insertImage, files) {
    const fd = new FormData()
    fd.append('file', files[0])

    this.$axios
      .post('/media/images/', fd)
      .then((res) => {
        this.$emit('image', res.data)
        insertImage({
          url: res.data.url,
          desc: 'desc',
        })
      })
      .catch((error) => {
        if (error.response.data.errors) {
          this.errors.push(...Object.values(error.response.data.errors))
        } else {
          console.log(error)
        }
      })
  }
}
</script>

<style scoped></style>
