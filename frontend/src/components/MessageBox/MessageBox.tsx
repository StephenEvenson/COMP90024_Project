import FlipMove from 'react-flip-move';
import React, {useEffect, useState} from "react";
import {BiMessageAltDots} from "react-icons/bi";
import {BsFillEmojiSmileFill, BsFillEmojiFrownFill, BsFillEmojiNeutralFill} from "react-icons/bs";
import useData from "../../hooks/useData";
import axios from "axios";

interface Message {
  id: string,
  content: string,
  sentiment_score: number,
  homeless_relative_score: number
}


function List(props: {
  items: Message [];
  removeItem: (index: number) => void;
}) {
  const {items, removeItem} = props;

  return (
    <FlipMove>
      {items.map((item, index) => (
        <div
          className='w-full rounded odd:bg-gray dark:bg-boxdark dark:text-body dark:odd:text-meta-2'
          key={item.id}
          onClick={() => removeItem(index)}
        >
          <div
            className='flex items-center justify-start px-2 py-0.5 text-sm whitespace-nowrap overflow-hidden overflow-ellipsis'>
            <div>
              {item.sentiment_score > 0.6 ? '😊' : item.sentiment_score < 0.4 ? '😔' : '😐'}
            </div>
            <div className='pl-1'>
              {item.content}
            </div>
          </div>
        </div>
      ))}
    </FlipMove>
  );
}

function RealTimeScrollingComponent(props: { max_num: number }) {
  const {max_num} = props;
  const [items, setItems] = useState([] as Message[]);

  // const [{data, isLoading, isError}, setUrl] =  useData('/mastodon/new', []);
  // console.log({data, isLoading, isError});
  // const messages = data as {id: string, text: string}[];
  const handleRemoveItem = (index: number) => {
    setItems((prevItems) => {
      const updatedItems = [...prevItems];
      updatedItems.splice(index, 1); // 从列表中删除指定索引的元素
      return updatedItems;
    });
  };
  // const fetchNewMessage = async () => {
  //   const newMessage = new Date().toLocaleTimeString();
  //   setItems(prevMessages => {
  //     return [...prevMessages, {id: prevMessages.length + 1 + newMessage, content: newMessage}]
  //   });
  // };
  // 每秒获取一次新消息
  useEffect(() => {
    const interval = 3;
    const intervalId = setInterval(async () => {
      const result = await axios(`/api/mastodon/new/${interval}`,);
      const newMessages = result.data.docs as Message[];
      // console.log(newMessages);
      const mess = newMessages.map((message) => (
        {
          id: message.id,
          content: message.content,
          sentiment_score: message.sentiment_score,
          homeless_relative_score: message.homeless_relative_score
        }
      ));
      setItems(prevMessages => {
        return [...prevMessages, ...mess]
      });
    }, interval * 1000);

    return () => clearInterval(intervalId);

  }, []);


  useEffect(() => {
    if (items.length > max_num) {
      handleRemoveItem(0)
    }
  }, [items]);

  return (
    <div
      className='rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark'>
      <div className='flex items-center space-x-2'>
        <BiMessageAltDots className='text-2xl fill-primary dark:fill-white'/>
        <div className='text-black-2 font-bold text-xl dark:text-white'>Mastodon Real Time Message:</div>
      </div>
      <div className='overflow-hidden h-55 px-2 space-y-0.5 xl:h-30'>
        <List items={items} removeItem={handleRemoveItem}></List>
      </div>
    </div>
  )
}

export default RealTimeScrollingComponent;