export interface PreviewQuestion {
  id: number
  title: string
  votes: number
  answers: number
  body: number
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
