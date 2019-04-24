

import api from '../config/ApiSauce'



export const getJobs = (termId) => {
  console.log(termId);
  
  return api.get('/terms/records', {
    params: {
      t: termId
    }
  })
}
