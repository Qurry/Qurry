export interface Tag {
  id: string
  name: string
  description: string
  color: string
}

export interface TreeNodeTag extends Tag {
  children: TreeNodeTag[]
}

export interface ObjectTag extends Tag {
  parentId: string
  childrenIds: string[]
}
