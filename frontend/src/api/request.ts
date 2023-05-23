import axios from 'axios';

export const request = axios.create({
  baseURL: "/api/"
})

export default request;