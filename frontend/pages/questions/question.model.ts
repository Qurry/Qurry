export interface PreviewQuestion {
  id: number
  title: string
  votes: number
  answers: number
  body: string
  dateTime: string
  user: {
    id: number
    username: string
  }
  tags: {
    id: number
    name: string
    description: string
  }[]
}

export interface CreateQuestion {
  title: string
  body: string
  tagIds: number[]
}
