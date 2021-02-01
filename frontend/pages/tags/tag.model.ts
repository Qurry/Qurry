export interface Tag {
  id: string
  name: string
  description: string
  color: string
}

export interface TreeTag extends Tag {
  children: TreeTag[]
}

export interface ObjectTag extends Tag {
  parentId: string
  childrenIds: string[]
}
