import {request} from "./request";
import {MessageItem, Sa4SudoHomeless, TwitterCount} from "../types";


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

export const getTwitterCount = async (type: 'all' | 'homeless' | 'abuse') => {
  const result = await request.get(`/twitter/count/${type}`);
  return result!.data!.count as TwitterCount;
}

export const getMastodonCount = async (type: 'all' | 'homeless' | 'abuse') => {
  const result = await request.get(`/mastodon/count/${type}`);
  const count = result!.data!.docs
  return {
    all: count.total,
    homeless: count.positive_homeless_scores,
    abuse: count.high_abusive_scores,
  } as TwitterCount;
}

export const getMastodonLangCount = async (interval: number) => {
  const result = await request.get(`/mastodon/lang/${interval}`);
  const count = result!.data!.docs
  return count;
}

export const getSa4SudoHomelessData = async (interval: number) => {
  const result = await request.get(`/sudo/sudo_sa4_homeless`);
  return result!.data!.docs as Sa4SudoHomeless[];
}