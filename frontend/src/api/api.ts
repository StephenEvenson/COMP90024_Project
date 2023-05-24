import {request} from "./request";
import {MessageItem, TwitterCount} from "../types";
import {queries} from "@testing-library/react";
import {config} from "react-transition-group";


export const getMastodonLatest = async (interval: number, source?: string) => {
  const result = await request.get(`/mastodon/new/${source}/${interval}`);
  return result!.data!.docs!.map((message: any) => ({
    id: message.id,
    content: message.content,
    sentiment_score: message.sentiment_score,
    homeless_relative_score: message.homeless_relative_score
  })) as MessageItem[];
}


export const getTwitterCount = async (type: 'all' | 'homeless' | 'language' | 'abuse') => {
  const result = await request.get(`/twitter/count/${type}`);
  return result!.data!.count as TwitterCount;
}

export const getMastodonCount = async (type: 'all' | 'homeless' | 'language' | 'abuse') => {
  const result = await request.get(`/twitter/count/${type}`);
  return result!.data!.count as TwitterCount;
}

