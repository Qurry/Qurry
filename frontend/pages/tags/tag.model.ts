export interface Tag {
  id: string
  name: string
  description: string
  color?: string
  children: Tag[]
}
