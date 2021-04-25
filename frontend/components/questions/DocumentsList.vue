<template>
  <div>
    <div v-for="document in documents" :key="document.id">
      <a :href="document.url" target="_blank">{{
        document.url.split('/').reverse()[0]
      }}</a>
      <DeleteDialog
        v-if="inFormMode"
        object-name="document"
        @delete="onDelete(document.id)"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { Document } from '~/pages/questions/question.model'

@Component
export default class DocumentsList extends Vue {
  @Prop()
  documents!: Document[]

  @Prop({ default: false })
  inFormMode!: boolean

  onDelete(imageId: string) {
    for (let i = 0; i < this.documents.length; i++) {
      if (imageId === this.documents[i].id) {
        this.documents.splice(i, 1)
      }
    }
  }
}
</script>

<style scoped></style>
