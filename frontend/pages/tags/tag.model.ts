export interface Tag {
  id: string
  name: string
  description?: string
}

export interface TagCategory {
  id: string
  name: string
  description?: string
  tags: Tag[]
}
