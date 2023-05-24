import {useState, useEffect} from 'react';
import axios from 'axios';

const baseUrl = "/api";


export default function useData(initialUrl: string, initialData: unknown): [{
  data: unknown,
  isLoading: boolean,
  isError: boolean
},
  React.Dispatch<React.SetStateAction<string>>
] {
  const [data, setData] = useState(initialData);
  const [url, setUrl] = useState(baseUrl + initialUrl);
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);


  useEffect(() => {
    const fetchData = async () => {
      setIsError(false);
      setIsLoading(true);
      try {
        const result = await axios(url);
        console.log(result.data);
        setData(result.data);
      } catch (error) {
        setIsError(true);
      }
      setIsLoading(false);
    };
    fetchData();
  }, [url]);
  return [{data, isLoading, isError}, setUrl];
}