export interface User {
  id: string
  username: string
}

export interface DetailQuestion {
  id: string
  title: string
  body: string
  votes: number
  userVote: number
  createDate: string
  editDate: string
  user: User
  tagIds: string[]
  answers: Answer[]
  comments: Comment[]
}

export interface PreviewQuestion {
  id: string
  title: string
  votes: number
  userVote: number
  answers: number
  comments: number
  createDate: string
  editDate: string
  user: User
  tagIds: string[]
}

export interface CreateEditQuestion {
  title: string
  body: string
  tagIds: number[]
}

export interface Answer {
  id: string
  createDate: string
  editDate: string
  body: string
  votes: number
  user: User
  userVote: number
  comments: Comment[]
}

export interface CreateEditAnswer {
  body: string
}

export interface Comment {
  id: string
  createDate: string
  editDate: string
  body: string
  user: User
}

export interface CreateEditComment {
  body: string
}
