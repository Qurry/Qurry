<template>
  <div>
    <img v-if="!isLoading" :src="'data:image;base64,' + base64Blob" />
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

@Component
export default class ImageUpload extends Vue {
  @Prop()
  uuid!: string

  base64Blob = ''
  isLoading = true

  created() {
    this.getImage()
  }

  async getImage() {
    const { data }: { data: any } = await this.$axios.get(
      '/media/images/' + this.uuid + '/'
    )
    this.base64Blob = data.data
    this.isLoading = false
  }
}
</script>

<style scoped></style>
