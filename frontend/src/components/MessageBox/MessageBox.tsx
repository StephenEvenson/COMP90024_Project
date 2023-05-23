import React, {useEffect, useState} from "react";
import FlipMove from 'react-flip-move';
import {BiMessageAltDots} from "react-icons/bi";
import {getMastodonLatest} from "../../api/api";
import {MessageItem} from "../../types";

function List(props: {
  items: MessageItem [];
  removeItem: (index: number) => void;
}) {
  const {items, removeItem} = props;

  return (
    <FlipMove>
      {items.map((item, index) => (
        <div
          className='w-full rounded odd:bg-gray dark:bg-boxdark dark:text-body dark:odd:text-meta-2'
          key={item.id + index}
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
    const interval = 3;
    const initData = async () => {
      const mess = await getMastodonLatest(interval) as MessageItem[];
      setItems(mess);
    }
    initData()

    const intervalId = setInterval(async () => {
      const mess = await getMastodonLatest(interval) as MessageItem[];
      setItems(prevMessages => [...prevMessages, ...mess]);
    }, interval * 1000);
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
        <div className='text-black-2 font-bold text-xl dark:text-white'>Mastodon Real Time Message:</div>
      </div>
      <div className='overflow-hidden h-55 px-2 space-y-0.5 xl:h-30'>
        <List items={items} removeItem={handleRemoveItem}></List>
      </div>
    </div>
  )
}

export default RealTimeScrollingComponent;