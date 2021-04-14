import { User } from './../users/user.model'

export interface Image {
  id: string
  url?: string
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
  documents: any[]
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
  documents: any[]
  tagIds: string[]
}

export interface QuestionSearch {
  limit: number
  page: number
  words: string
  tagIds: string[]
  orderBy: string
  answered: 'true' | 'false' | 'all'
}

export interface Answer {
  id: string
  createdAt: string
  editedAt: string
  body: string
  votes: number
  user: User
  userVote: number
  images: Image[]
  documents: any[]
  comments: Comment[]
}

export interface CreateEditAnswer {
  body: string
  images: Image[]
  documents: any[]
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

export interface Notification {
  id: string
  isRead: boolean
  message: string
  questionId: string
  objectId: string
  type: 'comment' | 'answer'
  createdAt: string
}
