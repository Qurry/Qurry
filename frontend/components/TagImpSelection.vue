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
  activeCategoryIds = new Set('1')
  categories: TagCategory[] = [
    {
      id: '1',
      name: 'Topic',
      color: 'blue',
      tags: [
        {
          id: '2',
          name: 'LV-Spezifisch',
          categoryImplications: ['3', '4', '5'],
        },
        {
          id: '22',
          name: 'Organisation',
          categoryImplications: ['7'],
        },
        {
          id: '1',
          name: 'Qurry',
          categoryImplications: ['2'],
        },
        {
          id: '3',
          name: 'Other',
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
          id: '29',
          name: 'discussion',
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
      name: 'Courses',
      color: 'pink',
      tags: [
        {
          id: '13',
          name: 'Theoretische Informatik I',
          categoryImplications: ['6'],
        },
        {
          id: '14',
          name: 'Internet Security - Weaknesses and Targets',
          categoryImplications: [],
        },
        {
          id: '15',
          name: 'Einführung in die Programmiertechnik I',
          categoryImplications: [],
        },
        {
          id: '16',
          name: 'other',
          categoryImplications: [],
        },
      ],
    },
    {
      id: '6',
      name: 'Theoretische Informatik I',
      color: 'orange',
      tags: [
        {
          id: '17',
          name: 'Berechenbarkeit',
          categoryImplications: [],
        },
        {
          id: '18',
          name: 'Algorithmik',
          categoryImplications: [],
        },
        {
          id: '19',
          name: 'Suchalgorithmen',
          categoryImplications: [],
        },
        {
          id: '20',
          name: 'Greedy',
          categoryImplications: [],
        },
        {
          id: '28',
          name: 'Meta',
          categoryImplications: [],
        },
        {
          id: '21',
          name: 'other',
          categoryImplications: [],
        },
      ],
    },
    {
      id: '7',
      name: 'Organisation',
      color: 'pink',
      tags: [
        {
          id: '23',
          name: 'Studienreferat',
          categoryImplications: [],
        },
        {
          id: '24',
          name: 'Wohnheim',
          categoryImplications: [],
        },
        {
          id: '25',
          name: 'Auslandssemester',
          categoryImplications: [],
        },
        {
          id: '26',
          name: 'Studentenclubs',
          categoryImplications: [],
        },
        {
          id: '27',
          name: 'other',
          categoryImplications: [],
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
    const updatedActiveCategoryIds = new Set('1')
    for (const selectedTagId of this.selectedTagIds) {
      this.getTag(selectedTagId)!.categoryImplications.forEach(
        updatedActiveCategoryIds.add,
        updatedActiveCategoryIds
      )
    }
    this.activeCategoryIds = updatedActiveCategoryIds
  }
}
</script>

<style scoped></style>
