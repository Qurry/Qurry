<template>
  <div class="tags">
    <p>{{ selectedTagIds }}</p>
    <v-row>
      <v-col v-for="categoryId of activeCategoryIds" :key="categoryId">
        <h3>{{ getCategory(categoryId).name }}</h3>
        <v-checkbox
          v-for="tag of getCategory(categoryId).tags"
          :key="tag.id"
          v-model="selectedTagIds"
          :label="tag.name"
          :value="tag.id"
          hide-details
          class="mt-0"
          @click="updateActiveCategoryIds"
        ></v-checkbox>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

export interface Tag {
  id: string
  name: string
  description?: string
  categoryId?: string
  categoryImplications: string[]
}

export interface TagCategoryImplication {
  categoryId: string
  allTags: boolean
  tagIds?: string[]
}

export interface TagCategory {
  id: string
  name: string
  description?: string
  color: string
  tags: Tag[]
}

@Component
export default class TagImpSelection extends Vue {
  selectedTagIds = []
  activeCategoryIds = ['1']
  categories: TagCategory[] = [
    {
      id: '1',
      name: 'Topic',
      color: 'blue',
      tags: [
        {
          id: '1',
          name: 'qurry',
          categoryImplications: ['2'],
        },
        {
          id: '2',
          name: 'LV-Spezifisch',
          categoryImplications: ['3', '4'],
        },
        {
          id: '3',
          name: 'other',
          categoryImplications: [],
        },
      ],
    },
    {
      id: '2',
      name: 'Qurry',
      color: 'orange',
      tags: [
        {
          id: '4',
          name: 'faq',
          categoryImplications: ['2'],
        },
        {
          id: '5',
          name: 'feature-request',
          categoryImplications: ['2'],
        },
        {
          id: '6',
          name: 'other',
          categoryImplications: ['2'],
        },
      ],
    },
    {
      id: '3',
      name: 'Semester',
      color: 'pink',
      tags: [
        {
          id: '7',
          name: 'wt20/21',
          categoryImplications: ['3', '4'],
        },
        {
          id: '8',
          name: 'st20',
          categoryImplications: ['3', '4'],
        },
        {
          id: '9',
          name: 'other',
          categoryImplications: ['3', '4'],
        },
      ],
    },
    {
      id: '4',
      name: 'Research Groups',
      color: 'pink',
      tags: [
        {
          id: '10',
          name: 'Algorithm Engineering',
          categoryImplications: ['3', '4'],
        },
        {
          id: '11',
          name: 'Internet Technologies and Systems',
          categoryImplications: ['3', '4'],
        },
        {
          id: '12',
          name: 'other',
          categoryImplications: ['3', '4'],
        },
      ],
    },
  ]

  getCategory(id: string): TagCategory | undefined {
    for (const category of this.categories) {
      if (category.id === id) {
        return category
      }
    }
  }

  getTag(id: string): Tag | undefined {
    for (const category of this.categories) {
      for (const tag of category.tags) {
        if (tag.id === id) {
          return tag
        }
      }
    }
  }

  updateActiveCategoryIds() {
    const updatedActiveCategoryIds: string[] = []
    for (const selectedTagId of this.selectedTagIds) {
      updatedActiveCategoryIds.push(
        ...this.getTag(selectedTagId)!.categoryImplications
      )
    }
    this.activeCategoryIds = updatedActiveCategoryIds
    if (!this.activeCategoryIds.includes('1')) {
      this.activeCategoryIds.push('1')
    }
  }
}
</script>

<style scoped></style>
