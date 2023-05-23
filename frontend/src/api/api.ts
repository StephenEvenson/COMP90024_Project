import {request} from "./request";
import {MessageItem} from "../types";


export const getMastodonLatest = async (interval: number) => {
  const result = await request.get(`/mastodon/new/${interval}`) as any;
  return result!.data!.docs!.map((message: any) => ({
    id: message.id,
    content: message.content,
    sentiment_score: message.sentiment_score,
    homeless_relative_score: message.homeless_relative_score
  })) as MessageItem[];
}

