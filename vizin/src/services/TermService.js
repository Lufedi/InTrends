

import api from '../config/ApiSauce'



export const getTerms = () => {
  return api.get('/terms')
}
