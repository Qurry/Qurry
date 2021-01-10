import { User } from './../users/user.model'

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
  imageIds: string[]
  documentIds?: string[]
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
  imageIds: string[]
  documentIds?: string[]
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
  imageIds?: string[]
  documentIds?: string[]
  comments: Comment[]
}

export interface CreateEditAnswer {
  body: string
  imageIds?: string[]
  documentIds?: string[]
}

export interface Comment {
  id: string
  createDcreatedAtate: string
  editedAt: string
  body: string
  user: User
}

export interface CreateEditComment {
  body: string
}
