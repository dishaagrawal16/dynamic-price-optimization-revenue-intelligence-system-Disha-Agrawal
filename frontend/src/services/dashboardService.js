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