import React, {useEffect, useState} from "react";
import FlipMove from 'react-flip-move';
import {BiMessageAltDots} from "react-icons/bi";
import {getMastodonLatest} from "../../api/api";
import {MessageItem} from "../../types";

function List(props: {
  items: MessageItem [];
  removeItem: (index: number) => void;
  server: string;
  sentiment?: boolean;
  homeless?: boolean;
}) {
  const {items, removeItem} = props;
  const sentiment = props.sentiment ?? true;
  const homeless = props.homeless ?? false;
  return (
    <FlipMove>
      {items.map((item, index) => (
        <div
          className='w-full rounded odd:bg-gray dark:bg-boxdark dark:text-body dark:odd:text-meta-2'
          key={`${props.server}_${item.id}_${index}`}
          onClick={() => removeItem(index)}
        >
          <div
            className='space-x-1 flex items-center justify-start px-2 py-0.5 text-sm'>
            {sentiment && (<div>
              {item.sentiment_score > 0.6 ? '😊' : item.sentiment_score < 0.4 ? '😔' : '😐'}
            </div>)}
            {homeless && (<div>
              {item.homeless_relative_score > 0 ? '🏠' : '🍀'}
            </div>)}
            <div
              className={'whitespace-nowrap overflow-hidden overflow-ellipsis ' + (item.abusive_score > 0.75 ? 'text-danger' : '')}>
              {item.abusive_score > 0.75 ? `#Vulgar#: ${item.abusive_score.toFixed(1)}` : ''} {item.content}
            </div>
          </div>
        </div>
      ))}
    </FlipMove>
  );
}

function RealTimeScrollingComponent(props: {
  max_num?: number,
  server?: string,
  interval?: number,
  className?: string,
  sentiment?: boolean;
  homeless?: boolean;
}) {
  const interval = props.interval || 5000;
  const max_num = props.max_num || 10;
  const server = props.server || '.au';
  const [items, setItems] = useState([] as MessageItem[]);

  const handleRemoveItem = (index: number) => {
    setItems((prevItems) => {
      const updatedItems = [...prevItems];
      updatedItems.splice(index, 1);
      return updatedItems;
    });
  };

  useEffect(() => {
    // fetch data from server every 3 seconds and update the state
    const initData = async () => {
      const mess = await getMastodonLatest(300, server) as MessageItem[];
      setItems([...mess].slice(mess.length - max_num, mess.length));
    }
    initData()

    const intervalId = setInterval(async () => {
      const mess = await getMastodonLatest(interval / 1000, server) as MessageItem[];
      setItems(prevMessages => [...prevMessages, ...mess]);
    }, interval);
    return () => clearInterval(intervalId);
  }, []);


  useEffect(() => {
    // make sure the number of items is less than max_num
    if (items.length > max_num) {
      handleRemoveItem(0)
    }
  }, [items]);

  return (
    <div
      className='rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark'>
      <div className='flex items-center space-x-2'>
        <BiMessageAltDots className='text-2xl fill-primary dark:fill-white'/>
        <div className='text-black-2 font-bold text-xl dark:text-white'>Mastodon Message Stream &nbsp;
          {server ? `(${server})` : undefined}:
        </div>
      </div>
      <div className={'overflow-hidden h-55 px-2 space-y-0.5 xl:h-30 ' + props.className}>
        <List
          items={items}
          removeItem={handleRemoveItem}
          server={server}
          homeless={props.homeless}
          sentiment={props.sentiment}/>
      </div>
    </div>
  )
}

export default RealTimeScrollingComponent;