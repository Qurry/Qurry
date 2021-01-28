<template>
  <div>
    <v-row justify="center" align="center">
      <v-col cols="8">
        <v-file-input
          v-model="currentFile"
          show-size
          label="Select File"
          color="secondary"
        ></v-file-input>
      </v-col>

      <v-col cols="4" class="pl-2">
        <v-btn
          :disabled="!currentFile || isUploading"
          :loading="isUploading"
          color="secondary"
          small
          @click="upload"
        >
          Upload
          <v-icon right dark>mdi-cloud-upload</v-icon>
        </v-btn>
      </v-col>
    </v-row>

    <MessageList :messages="errors" />

    <template v-if="images.length > 0" class="mx-auto">
      <div v-for="image in images" :key="image.id">
        <img :src="image.url" alt="Couldn't load image" />
        <span>{{ image.id }}</span>
        <DeleteDialog object-name="image" @delete="onDelete(image.id)" />
      </div>
    </template>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { Image } from './../pages/questions/question.model'

@Component
export default class ImageUpload extends Vue {
  currentFile: any = null
  errors: string[] = []
  isUploading = false

  @Prop()
  images!: Image[]

  onDelete(imageId: string) {
    for (let i = 0; i < this.images.length; i++) {
      if (imageId === this.images[i].id) {
        this.images.splice(i, 1)
      }
    }
  }

  upload() {
    if (!this.currentFile) {
      this.errors.push('Please select a file!')
      return
    }
    this.errors = []
    this.isUploading = true

    const fd = new FormData()
    fd.append('file', this.currentFile, this.currentFile.name)

    this.$axios
      .post('/media/images/', fd)
      .then((res) => {
        this.images.push({ id: res.data.imageId })
        this.currentFile = null
        this.isUploading = false
      })
      .catch((error) => {
        if (error.response.data.errors) {
          this.errors.push(
            ...Object.values(error.response.data.errors as string)
          )
        } else {
          console.log(error)
        }
        this.currentFile = null
        this.isUploading = false
      })
  }
}
</script>
