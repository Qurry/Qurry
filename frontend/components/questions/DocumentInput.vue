<template>
  <div>
    <h2 class="mt-3">Documents</h2>
    <div class="input-row">
      <v-file-input
        v-model="documentToUpload"
        label="Select Document"
      ></v-file-input>
      <v-btn
        color="secondary"
        :disabled="!documentToUpload"
        :loading="isLoading"
        class="ml-3 mt-2"
        @click="uploadDocument"
      >
        Upload
      </v-btn>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component
export default class DocumentInput extends Vue {
  documentToUpload = null
  isLoading = false

  uploadDocument() {
    this.isLoading = true
    const fd = new FormData()
    fd.append('file', this.documentToUpload!)

    this.$axios
      .post('/media/documents/', fd)
      .then((res) => {
        this.$emit('document', res.data)
      })
      .catch((error) => {
        console.log(error)
      })
      .finally(() => {
        this.isLoading = false
        this.documentToUpload = null
      })
  }
}
</script>

<style scoped>
.input-row {
  display: flex;
}
</style>
