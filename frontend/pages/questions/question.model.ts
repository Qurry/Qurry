export interface PreviewQuestion {
  id: number
  title: string
  votes: number
  answers: number
  dateTime?: string
  user: {
    id: number
    name: string
  }
  tags: {
    id: number
    name: string
  }[]
}
