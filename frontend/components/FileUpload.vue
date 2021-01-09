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
        <p v-if="isUploading">Uploading...</p>
        <v-btn
          v-else
          :disabled="!currentFile"
          color="secondary"
          small
          @click="upload"
        >
          Upload
          <v-icon right dark>mdi-cloud-upload</v-icon>
        </v-btn>
      </v-col>
    </v-row>

    <v-alert v-if="message" border="left" color="blue-grey" dark>
      {{ message }}
    </v-alert>

    <!-- <template v-if="uploadedFiles.length > 0" class="mx-auto">
      <div v-for="file in uploadedFiles" :key="file.uuid">
        <p>{{ file.localId }} - {{ file.uuid }}</p>
        <PrettyImage :uuid="file.uuid" />
      </div>
    </template> -->
    <template v-if="imageIds.length > 0" class="mx-auto">
      <div v-for="imageId in imageIds" :key="imageId">
        <p>{{ imageId }}</p>
        <PostImage :uuid="imageId" />
      </div>
    </template>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

interface File {
  localId: string
  uuid: string
}

@Component
export default class FileUpload extends Vue {
  currentFile: any = null
  message = ''
  // uploadedFiles: File[] = []
  isUploading = false

  @Prop()
  imageIds!: string[]

  upload() {
    if (!this.currentFile) {
      this.message = 'Please select a file!'
      return
    }
    this.message = ''

    this.isUploading = true

    const fd = new FormData()
    fd.append('file', this.currentFile, this.currentFile.name)

    this.$axios
      .post('/media/images/', fd)
      .then((res) => {
        // this.uploadedFiles.push({
        //   localId: (this.uploadedFiles.length + 1).toString(),
        //   uuid: res.data.imageId,
        // })
        this.imageIds.push(res.data.imageId)
        this.currentFile = null
        this.isUploading = false
      })
      .catch(() => {
        this.message = 'Could not upload the file!'
        this.currentFile = null
        this.isUploading = false
      })
  }
}
</script>
