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
  high_abusive_scores: number,
}

export interface MastodonCount {
  all: number,
  positive_homeless_scores: number,
  high_abusive_scores: number,
}

export interface Sa4GeoData {
  FeatureCollection: string,
  features: any[],
}