<template>
  <span v-if="!error">
    <span v-if="!!image.src">
      <img
        :src="
          image.type === 'url-image' ? image.src : !!idImage ? idImage.url : ''
        "
        :title="image.description"
        class="post-image"
        @error="addError"
      />
    </span>
  </span>
  <span v-else class="image-error">
    COULD NOT LOAD IMAGE WITH
    {{ image.type === 'url-image' ? 'URL' : 'ID' }} {{ image.src }}
  </span>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { ImageContent } from '../mixins/contentParser'
import { Image } from './../pages/questions/question.model'

@Component
export default class PostImageClass extends Vue {
  error = false

  @Prop()
  image!: ImageContent

  @Prop()
  idImage!: Image

  addError() {
    this.error = true
  }
}
</script>

<style scoped>
.post-image {
  max-width: 100%;
}
.image-error {
  background-color: rgb(255, 194, 194);
}
</style>
