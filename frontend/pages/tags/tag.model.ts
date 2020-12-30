export interface Tag {
  id: string
  name: string
  description?: string
  color: string
  tagCategoryId: string
}

export interface TagCategory {
  id: string
  name: string
  description?: string
  color: string
  tags: Tag[]
}
