import api from "./api";

export const getDashboardSummary = async () => {
    const response = await api.get("/dashboard/summary");
    return response.data;
};
export const getMonthlyRevenue = async () => {
    const response = await api.get("/dashboard/monthly-revenue");
    return response.data;
};

export const getCategoryRevenue = async () => {
    const response = await api.get("/dashboard/category-revenue");
    return response.data;
};

export const getRecentProducts = async () => {
    const response = await api.get("/dashboard/recent-products");
    return response.data;
};

export const getPaymentDistribution = async () => {
    const response = await api.get("/dashboard/payment-distribution");
    return response.data;
};



export const getCompetitorSummary = async () => {
  const response = await api.get("/competitor/summary");
  return response.data;
};

export const getCompetitorComparison = async () => {
  const response = await api.get("/competitor/comparison");
  return response.data;
};

export const getCompetitorProducts = async () => {
  const response = await api.get("/competitor/products");
  return response.data;
};

export const getCategoryCompetitorPrices = async () => {
  const response = await api.get("/competitor/category-prices");
  return response.data;
};

export const getMarketIntelligence = async () => {

  const response = await api.get(
    "/competitor/market-intelligence"
  );

  return response.data;
};

export const getProfitabilitySummary = async () => {

  const response = await api.get(
    "/profitability/summary"
  );

  return response.data;

};


export const getCategoryProfitability = async () => {

  const response = await api.get(
    "/profitability/category-analysis"
  );

  return response.data;

};

export const getPricingRecommendations = async () => {

  const response = await api.get(
    "/pricing-strategy/recommendations"
  );

  return response.data;

};

export const getExecutiveSummary = async () => {

  const response = await api.get(
    "/executive-report/summary"
  );

  return response.data;

};


export const getExecutiveCategoryAnalysis = async () => {

  const response = await api.get(
    "/executive-report/category-analysis"
  );

  return response.data;

};