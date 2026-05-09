import axios from 'axios'

export async function createCheckoutSession(planType) {
  const res = await axios.post('/api/payment/create-checkout', {
    plan_type: planType,
  })
  return res.data.data
}
