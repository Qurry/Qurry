export interface PreviewQuestion {
  id: string
  title: string
  votes: number
  answers: number
  dateTime: string
  user: {
    id: number
    username: string
  }
  tagIds: string[]
}

export interface Answer {
  id: string
  body: string
  dateTime: string
  votes: number
  user: {
    id: number
    username: string
  }
}

export interface DetailQuestion {
  id: string
  title: string
  body: string
  votes: number
  dateTime: string
  user: {
    id: number
    username: string
  }
  tagIds: string[]
  answers: Answer[]
}

export interface CreateEditQuestion {
  title: string
  body: string
  tagIds: number[]
}
