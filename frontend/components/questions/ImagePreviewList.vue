<template>
  <div v-if="images.length > 0">
    <h2 class="mt-3">Images</h2>
    <div class="image-preview-container">
      <template class="mx-auto">
        <div
          v-for="image in images"
          :key="image.id"
          class="image-preview-outer-box"
        >
          <div class="image-preview-inner-box">
            <img
              :src="image.url"
              alt="Couldn't load image"
              class="image-preview"
            />
          </div>
          <v-btn
            icon
            color="secondary"
            @click.stop.prevent="copyImageUrl(image.url)"
          >
            <v-icon>mdi-content-copy</v-icon>
          </v-btn>
          <DeleteDialog object-name="image" @delete="onDelete(image.id)" />
        </div>
      </template>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { Image } from '~/pages/questions/question.model'

@Component
export default class ImagePreviewList extends Vue {
  @Prop()
  images!: Image[]

  copyImageUrl(imageUrl: string) {
    const dummy = document.createElement('textarea')
    document.body.appendChild(dummy)
    dummy.value = imageUrl
    dummy.select()
    document.execCommand('copy')
    document.body.removeChild(dummy)
  }

  onDelete(imageId: string) {
    for (let i = 0; i < this.images.length; i++) {
      if (imageId === this.images[i].id) {
        this.images.splice(i, 1)
      }
    }
  }
}
</script>

<style scoped>
.image-preview-container {
  display: flex;
  flex-wrap: wrap;
}

.image-preview-outer-box {
  border: 1px solid #ccc;
  margin-right: 5px;
}

.image-preview-inner-box {
  width: 100px;
  height: 101px;
  border-bottom: 1px solid #ccc;
}

.image-preview {
  max-width: 100px;
  max-height: 100px;
}
</style>
