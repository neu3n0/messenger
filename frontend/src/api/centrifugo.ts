import api from './axios';


export const getCentrifugoToken = async () => {
  const response = await api.get("/centrifugo_token/connection/", {});
  return response.data.token;
}


export const getSubscriptionToken = async (channel: string) => {
  const response = await api.get("/centrifugo_token/subscription/", {
    params: { channel: channel }
  });
  return response.data.token;
}