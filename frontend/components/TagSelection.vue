<template>
  <div class="tags">
    <h2>Select your Tags</h2>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
// import { Tag } from './../pages/tags/tag.model'

export interface Tag {
  id: string
  name: string
  description?: string
  categoryId?: string
  categoryImplications: TagCategoryImplication[]
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
export default class TagSelection extends Vue {
  tagCategories: TagCategory[] = [
    {
      id: '1',
      name: 'Topic',
      color: 'blue',
      tags: [
        {
          id: '1',
          name: 'qurry',
          categoryImplications: [
            {
              categoryId: '2',
              allTags: true,
            },
          ],
        },
        {
          id: '2',
          name: 'LV-Spezifisch',
          categoryImplications: [],
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
          categoryImplications: [],
        },
        {
          id: '5',
          name: 'feature-request',
          categoryImplications: [],
        },
        {
          id: '6',
          name: 'other',
          categoryImplications: [],
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
          categoryImplications: [],
        },
        {
          id: '8',
          name: 'st20',
          categoryImplications: [],
        },
        {
          id: '9',
          name: 'other',
          categoryImplications: [],
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
          categoryImplications: [],
        },
        {
          id: '11',
          name: 'Internet Technologies and Systems',
          categoryImplications: [],
        },
        {
          id: '12',
          name: 'other',
          categoryImplications: [],
        },
      ],
    },
    {
      id: '5',
      name: 'Research Groups',
      color: 'pink',
      tags: [
        {
          id: '10',
          name: 'Algorithm Engineering',
          categoryImplications: [],
        },
        {
          id: '11',
          name: 'Internet Technologies and Systems',
          categoryImplications: [],
        },
        {
          id: '12',
          name: 'other',
          categoryImplications: [],
        },
      ],
    },
  ]
}
</script>

<style scoped></style>
