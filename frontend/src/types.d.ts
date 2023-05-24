export interface MessageItem {
  id: string,
  content: string,
  created_at: string,
  abusive_score: number,
  sentiment_score: number,
  homeless_relative_score: number,
}

export interface TwitterCount {
  all: number,
  homeless: number,
  language: number,
  abuse: number
}