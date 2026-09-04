import api from "./api";


export const predictPrice = async (data) => {
  const response = await api.post(
    "/prediction/predict-price",
    data
  );

  return response.data;
};