export interface DetailQuestion {
  id: string
  title: string
  body: string
  votes: number
  userVote: number
  dateTime: string
  user: {
    id: number
    username: string
  }
  tagIds: string[]
  answers: Answer[]
}

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

export interface CreateEditQuestion {
  title: string
  body: string
  tagIds: number[]
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
  userVote: number
}

export interface CreateEditAnswer {
  body: string
}
