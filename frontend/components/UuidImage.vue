<template>
  <img
    v-if="!isLoading"
    :src="'data:image;base64,' + base64Blob"
    :width="width ? width : ''"
    :height="height ? height : ''"
  />
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

@Component
export default class UuidImage extends Vue {
  @Prop()
  uuid!: string

  @Prop()
  width!: string

  @Prop()
  height!: string

  base64Blob = ''
  isLoading = true

  created() {
    this.getImage()
  }

  async getImage() {
    const { data }: { data: any } = await this.$axios.get(
      '/media/images/' + this.uuid + '/'
    )
    this.base64Blob = Buffer.from(data.data, 'hex').toString('base64')
    this.isLoading = false
  }
}
</script>

<style scoped></style>
