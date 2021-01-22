<template>
  <img
    v-if="!isLoading"
    :src="url"
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

  url = ''
  isLoading = true

  created() {
    this.getImage()
  }

  async getImage() {
    const { data }: { data: any } = await this.$axios.get(
      '/media/images/' + this.uuid + '/'
    )
    this.url = data.imageUrl
    this.isLoading = false
  }
}
</script>

<style scoped></style>
