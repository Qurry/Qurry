import { User } from './../users/user.model'

export interface Image {
  id: string
  localId?: string
  url?: string
  description?: string
}

export interface DetailQuestion {
  id: string
  title: string
  body: string
  votes: number
  userVote: number
  createdAt: string
  editedAt: string
  user: User
  tagIds: string[]
  images: Image[]
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
  createdAt: string
  editedAt: string
  user: User
  tagIds: string[]
}

export interface CreateEditQuestion {
  title: string
  body: string
  images: Image[]
  tagIds: string[]
}

export interface QuestionSearch {
  text: string
  tagIds: string[]
}

export interface Answer {
  id: string
  createdAt: string
  editedAt: string
  body: string
  votes: number
  user: User
  userVote: number
  images?: Image[]
  comments: Comment[]
}

export interface CreateEditAnswer {
  body: string
  images?: Image[]
}

export interface Comment {
  id: string
  createdAt: string
  editedAt: string
  body: string
  user: User
}

export interface CreateEditComment {
  body: string
}
