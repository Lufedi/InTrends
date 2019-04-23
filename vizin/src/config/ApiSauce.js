
import axios from 'axios'
const instance = axios.create({
    baseURL: 'https://in-trends.herokuapp.com',
    timeout: 30000,
  });



export default instance