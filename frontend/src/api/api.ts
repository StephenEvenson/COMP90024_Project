import {request} from "./request";
import {MastodonCount, MessageItem, Sa4SudoHomeless, TwitterCount} from "../types";


export const getMastodonLatest = async (interval: number, source?: string) => {
  const result = await request.get(`/mastodon/new/${source}/${interval}`);
  return result!.data!.docs!.map((message: any) => ({
    id: message.id,
    content: message.content,
    abusive_score: message.abusive_score,
    sentiment_score: message.sentiment_score,
    homeless_relative_score: message.homeless_relative_score,
  })) as MessageItem[];
}

export const getTwitterCount = async (type: 'all' | 'homeless') => {
  const result = await request.get(`/twitter/count/${type}`);
  return result!.data!.docs as TwitterCount;
}

export const getMastodonCount = async (type: 'all' | 'homeless' | 'abuse') => {
  const result = await request.get(`/mastodon/count/${type}`);
  const count = result!.data!.docs
  return {
    all: count.total,
    positive_homeless_scores: count.positive_homeless_scores,
    high_abusive_scores: count.high_abusive_scores,
  } as MastodonCount;
}

export const getMastodonLangCount = async (interval: number) => {
  const result = await request.get(`/mastodon/lang/${interval}`);
  return result!.data!.docs
}

export const getSa4SudoHomelessData = async () => {
  const result = await request.get(`/sudo/sudo_sa4_homeless`);
  return result!.data!.docs as Sa4SudoHomeless[];
}

export const getHomelessFactors = async (area?: string) => {
  const result = await request.get(`/twitter/homeless/distribution/${area || 'all'}`);
  return result!.data!.docs;
}

export const getTwitterSentimentPeriod = async (period: string) => {
  const result = await request.get(`/twitter/sentiment/period/${period}`);
  return result!.data!.docs;
}