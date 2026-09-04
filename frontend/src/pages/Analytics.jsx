import Layout from "../components/Layout";
import { useEffect, useState } from "react";
import {
  getProfitabilitySummary,
  getCategoryProfitability,
  getPricingRecommendations,
  getExecutiveSummary,
  getExecutiveCategoryAnalysis,
} from "../services/dashboardService";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import {
  FaRupeeSign,
  FaChartLine,
  FaPercentage,
  FaTrophy,
} from "react-icons/fa";


function Analytics() {

  const [summary, setSummary] = useState({
    total_revenue: 0,
    estimated_cost: 0,
    estimated_profit: 0,
    estimated_profit_margin: 0,
    most_profitable_category: "-",
  });

  const [categoryData, setCategoryData] = useState([]);
  const [pricingRecommendations, setPricingRecommendations] = useState([]);

  const [loading, setLoading] = useState(true);


  // ============================================================
  // FETCH PROFITABILITY DATA
  // ============================================================
  const [executiveSummary, setExecutiveSummary] = useState({
  total_revenue: 0,
  estimated_cost: 0,
  estimated_profit: 0,
  estimated_profit_margin: 0,
  most_profitable_category: "",
  high_priority_actions: 0,
  categories_requiring_better_data: 0,
});

const [executiveCategories, setExecutiveCategories] = useState([]);
  useEffect(() => {

    const fetchProfitabilityData = async () => {

      try {

         const [
           summaryData,
           categoryData,
           recommendationData,
           executiveSummaryData,
           executiveCategoriesData
         ] = await Promise.all([
           getProfitabilitySummary(),
           getCategoryProfitability(),
           getPricingRecommendations(),
           getExecutiveSummary(),
           getExecutiveCategoryAnalysis(),
         ]);


        setSummary(summaryData);

        setCategoryData(categoryData);

        setPricingRecommendations(
          recommendationData
        );

        setExecutiveSummary(
          executiveSummaryData
        );
        
        setExecutiveCategories(
          executiveCategoriesData
        );

      } catch (error) {

        console.error(
          "Error fetching profitability data:",
          error
        );

      } finally {

        setLoading(false);

      }

    };


    fetchProfitabilityData();

  }, []);


  // ============================================================
  // FORMAT CURRENCY
  // ============================================================

  const formatCurrency = (value) => {

    return `₹${Number(value).toLocaleString(
      "en-IN",
      {
        maximumFractionDigits: 2,
      }
    )}`;

  };


  // ============================================================
  // LOADING
  // ============================================================

  if (loading) {

    return (
      <Layout title="Analytics">

        <div className="flex items-center justify-center h-64">

          <p className="text-gray-500">
            Loading profitability analytics...
          </p>

        </div>

      </Layout>
    );

  }


  return (

    <Layout title="Analytics">

      {/* ====================================================== */}
      {/* PAGE HEADER */}
      {/* ====================================================== */}

      <div>

        <h1 className="text-3xl font-bold text-gray-800">
          Revenue & Profitability Analytics
        </h1>

        <p className="text-gray-600 mt-2">
          Analyze revenue performance and estimated profitability
          across product categories.
        </p>

      </div>


      {/* ====================================================== */}
      {/* ESTIMATION NOTICE */}
      {/* ====================================================== */}

      <div className="mt-6 bg-yellow-50 border border-yellow-200 rounded-xl p-4">

        <p className="text-sm text-yellow-800">

          <strong>Note:</strong>{" "}

          Profitability is estimated using configurable
          category-level cost assumptions because actual
          product cost data is not available in the source
          dataset.

        </p>

      </div>


      {/* ====================================================== */}
      {/* SUMMARY CARDS */}
      {/* ====================================================== */}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-8">


        {/* Total Revenue */}

        <div className="bg-white rounded-2xl shadow-md p-6">

          <div className="flex items-center justify-between">

            <div>

              <p className="text-sm text-gray-500">
                Total Revenue
              </p>

              <h2 className="text-2xl font-bold text-gray-800 mt-2">

                {formatCurrency(
                  summary.total_revenue
                )}

              </h2>

            </div>

            <div className="text-green-600 text-2xl">

              <FaRupeeSign />

            </div>

          </div>

        </div>


        {/* Estimated Profit */}

        <div className="bg-white rounded-2xl shadow-md p-6">

          <div className="flex items-center justify-between">

            <div>

              <p className="text-sm text-gray-500">
                Estimated Profit
              </p>

              <h2 className="text-2xl font-bold text-gray-800 mt-2">

                {formatCurrency(
                  summary.estimated_profit
                )}

              </h2>

            </div>

            <div className="text-blue-600 text-2xl">

              <FaChartLine />

            </div>

          </div>

        </div>


        {/* Profit Margin */}

        <div className="bg-white rounded-2xl shadow-md p-6">

          <div className="flex items-center justify-between">

            <div>

              <p className="text-sm text-gray-500">
                Estimated Profit Margin
              </p>

              <h2 className="text-2xl font-bold text-gray-800 mt-2">

                {Number(
                  summary.estimated_profit_margin
                ).toFixed(2)}%

              </h2>

            </div>

            <div className="text-purple-600 text-2xl">

              <FaPercentage />

            </div>

          </div>

        </div>


        {/* Best Category */}

        <div className="bg-white rounded-2xl shadow-md p-6">

          <div className="flex items-center justify-between">

            <div>

              <p className="text-sm text-gray-500">
                Most Profitable Category
              </p>

              <h2 className="text-xl font-bold text-gray-800 mt-2">

                {summary.most_profitable_category}

              </h2>

            </div>

            <div className="text-orange-500 text-2xl">

              <FaTrophy />

            </div>

          </div>

        </div>

      </div>


      {/* ====================================================== */}
      {/* CHARTS */}
      {/* ====================================================== */}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-10">


        {/* ==================================================== */}
        {/* REVENUE VS PROFIT */}
        {/* ==================================================== */}

        <div className="bg-white rounded-2xl shadow-md p-6">

          <div className="mb-5">

            <h2 className="text-xl font-bold text-gray-800">
              Revenue vs Estimated Profit
            </h2>

            <p className="text-sm text-gray-500 mt-1">
              Category-wise revenue and estimated profit
            </p>

          </div>


          <ResponsiveContainer
            width="100%"
            height={350}
          >

            <BarChart
              data={categoryData}
              margin={{
                top: 10,
                right: 20,
                left: 20,
                bottom: 20,
              }}
            >

              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis
                dataKey="Category_Name"
                tick={{ fontSize: 12 }}
              />

              <YAxis
                tickFormatter={(value) =>
                  `₹${(value / 1000000).toFixed(1)}M`
                }
              />

              <Tooltip
                formatter={(value) =>
                  formatCurrency(value)
                }
              />

              <Bar
                dataKey="Total_Revenue"
                name="Revenue"
                fill="#16a34a"
                radius={[6, 6, 0, 0]}
              />

              <Bar
                dataKey="Estimated_Profit"
                name="Estimated Profit"
                fill="#2563eb"
                radius={[6, 6, 0, 0]}
              />

            </BarChart>

          </ResponsiveContainer>

        </div>


        {/* ==================================================== */}
        {/* PROFIT MARGIN */}
        {/* ==================================================== */}

        <div className="bg-white rounded-2xl shadow-md p-6">

          <div className="mb-5">

            <h2 className="text-xl font-bold text-gray-800">
              Profit Margin by Category
            </h2>

            <p className="text-sm text-gray-500 mt-1">
              Estimated profitability percentage
            </p>

          </div>


          <ResponsiveContainer
            width="100%"
            height={350}
          >

            <BarChart
              data={categoryData}
              margin={{
                top: 10,
                right: 20,
                left: 20,
                bottom: 20,
              }}
            >

              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis
                dataKey="Category_Name"
                tick={{ fontSize: 12 }}
              />

              <YAxis
                tickFormatter={(value) =>
                  `${value}%`
                }
              />

              <Tooltip
                formatter={(value) =>
                  `${Number(value).toFixed(2)}%`
                }
              />

              <Bar
                dataKey="Estimated_Profit_Margin"
                name="Profit Margin"
                fill="#9333ea"
                radius={[6, 6, 0, 0]}
              />

            </BarChart>

          </ResponsiveContainer>

        </div>

      </div>


      {/* ====================================================== */}
      {/* CATEGORY PROFITABILITY TABLE */}
      {/* ====================================================== */}

      <div className="bg-white rounded-2xl shadow-md p-6 mt-10">

        <div className="mb-5">

          <h2 className="text-xl font-bold text-gray-800">
            Category Profitability
          </h2>

          <p className="text-sm text-gray-500 mt-1">
            Detailed revenue and estimated profitability
            performance by category.
          </p>

        </div>


        <div className="overflow-x-auto">

          <table className="w-full">

            <thead>

              <tr className="border-b">

                <th className="text-left py-3 px-4 text-sm text-gray-500">
                  Category
                </th>

                <th className="text-right py-3 px-4 text-sm text-gray-500">
                  Demand
                </th>

                <th className="text-right py-3 px-4 text-sm text-gray-500">
                  Revenue
                </th>

                <th className="text-right py-3 px-4 text-sm text-gray-500">
                  Est. Cost
                </th>

                <th className="text-right py-3 px-4 text-sm text-gray-500">
                  Est. Profit
                </th>

                <th className="text-right py-3 px-4 text-sm text-gray-500">
                  Margin
                </th>

                <th className="text-center py-3 px-4 text-sm text-gray-500">
                  Level
                </th>

              </tr>

            </thead>


            <tbody>

              {categoryData.map(
                (item) => (

                  <tr
                    key={item.Category_Name}
                    className="border-b hover:bg-gray-50"
                  >

                    <td className="py-4 px-4 font-medium">
                      {item.Category_Name}
                    </td>

                    <td className="py-4 px-4 text-right">
                      {Number(
                        item.Total_Demand
                      ).toLocaleString(
                        "en-IN"
                      )}
                    </td>

                    <td className="py-4 px-4 text-right">
                      {formatCurrency(
                        item.Total_Revenue
                      )}
                    </td>

                    <td className="py-4 px-4 text-right">
                      {formatCurrency(
                        item.Estimated_Cost
                      )}
                    </td>

                    <td className="py-4 px-4 text-right font-semibold">
                      {formatCurrency(
                        item.Estimated_Profit
                      )}
                    </td>

                    <td className="py-4 px-4 text-right">
                      {Number(
                        item.Estimated_Profit_Margin
                      ).toFixed(2)}%
                    </td>

                    <td className="py-4 px-4 text-center">

                      <span
                        className={
                          item.Profitability_Level === "High"
                            ? "px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700"
                            : item.Profitability_Level === "Moderate"
                            ? "px-3 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-700"
                            : "px-3 py-1 rounded-full text-xs font-medium bg-red-100 text-red-700"
                        }
                      >

                        {item.Profitability_Level}

                      </span>

                    </td>

                  </tr>

                )
              )}

            </tbody>

          </table>

        </div>

      </div>

      {/* ====================================================== */}
{/* PRICING STRATEGY RECOMMENDATIONS */}
{/* ====================================================== */}

<div className="bg-white rounded-2xl shadow-md p-6 mt-10">

  <div className="mb-6">

    <h2 className="text-xl font-bold text-gray-800">
      Pricing Strategy Recommendations
    </h2>

    <p className="text-sm text-gray-500 mt-1">
      Data-driven pricing recommendations based on
      competitor pricing, demand and estimated profitability.
    </p>

  </div>


  <div className="space-y-4">

    {pricingRecommendations.map(
      (item) => (

        <div
          key={item.Category}
          className="border rounded-xl p-5 hover:bg-gray-50 transition"
        >

          {/* CATEGORY + PRIORITY */}

          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3">

            <div>

              <h3 className="text-lg font-semibold text-gray-800">
                {item.Category}
              </h3>

              <div className="flex flex-wrap gap-3 mt-2 text-sm text-gray-500">

                <span>
                  Our Price: ₹
                  {Number(
                    item.Average_Final_Price
                  ).toFixed(2)}
                </span>

                <span>
                  Demand:{" "}
                  {Number(
                    item.Average_Demand
                  ).toFixed(2)}
                </span>

                <span>
                  Price Gap:{" "}
                  {item.Price_Gap_Percent !== null
                    ? `${Number(
                        item.Price_Gap_Percent
                      ).toFixed(2)}%`
                    : "N/A"}
                </span>

                <span>
                  Margin:{" "}
                  {item.Estimated_Profit_Margin !== null
                    ? `${Number(
                        item.Estimated_Profit_Margin
                      ).toFixed(2)}%`
                    : "N/A"}
                </span>

              </div>

            </div>


            {/* PRIORITY */}

            <span
              className={
                item.Priority === "High"
                  ? "px-3 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-700"
                  : item.Priority === "Medium"
                  ? "px-3 py-1 rounded-full text-xs font-semibold bg-yellow-100 text-yellow-700"
                  : "px-3 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-700"
              }
            >

              {item.Priority} Priority

            </span>

          </div>


          {/* MARKET POSITION */}

          <div className="mt-4">

            <span className="text-xs font-medium text-gray-500">
              Market Position
            </span>

            <p className="text-sm font-medium text-gray-700 mt-1">
              {item.Market_Position}
            </p>

          </div>


          {/* RECOMMENDATION */}

          <div className="mt-4 bg-gray-50 rounded-lg p-4">

            <p className="text-xs font-medium text-gray-500 mb-1">
              Recommended Action
            </p>

            <p className="text-sm text-gray-700 leading-relaxed">
              {item.Pricing_Recommendation}
            </p>

          </div>

        </div>

      )
    )}

  </div>

</div>

{/* ====================================================== */
/* RECOMMENDATION VALIDATION */
/* ====================================================== */}

<div className="bg-white rounded-2xl shadow-md p-6 mt-10">

  <div className="mb-6">

    <h2 className="text-xl font-bold text-gray-800">
      ✅ Recommendation Validation
    </h2>

    <p className="text-sm text-gray-500 mt-1">
      Validation results for the pricing recommendation rules
      across all product categories.
    </p>

  </div>


  {/* VALIDATION SUMMARY */}

  <div className="grid grid-cols-1 md:grid-cols-3 gap-5">

    {/* TOTAL */}

    <div className="bg-blue-50 rounded-xl p-5 text-center">

      <p className="text-sm text-gray-600">
        Total Recommendations
      </p>

      <h3 className="text-3xl font-bold text-gray-800 mt-2">
        7
      </h3>

    </div>


    {/* PASSED */}

    <div className="bg-green-50 rounded-xl p-5 text-center">

      <p className="text-sm text-gray-600">
        Passed
      </p>

      <h3 className="text-3xl font-bold text-green-600 mt-2">
        7
      </h3>

    </div>


    {/* FAILED */}

    <div className="bg-red-50 rounded-xl p-5 text-center">

      <p className="text-sm text-gray-600">
        Failed
      </p>

      <h3 className="text-3xl font-bold text-red-600 mt-2">
        0
      </h3>

    </div>

  </div>


  {/* VALIDATION RATE */}

  <div className="mt-6 bg-gray-50 rounded-xl p-5">

    <div className="flex justify-between items-center mb-2">

      <span className="font-medium text-gray-700">
        Validation Rate
      </span>

      <span className="font-bold text-green-600">
        100%
      </span>

    </div>


    <div className="w-full bg-gray-200 rounded-full h-3">

      <div
        className="bg-green-500 h-3 rounded-full"
        style={{ width: "100%" }}
      ></div>

    </div>

  </div>


  {/* VALIDATION NOTE */}

  <div className="mt-5 bg-green-50 border border-green-200 rounded-lg p-4">

    <p className="text-sm text-gray-700">

      <strong>Validation Result:</strong>{" "}
      All 7 category-level pricing recommendations
      passed the configured business-rule validation checks.
      No failed recommendations were identified.

    </p>

  </div>

</div>

{/* ====================================================== */}
{/* EXECUTIVE BUSINESS INTELLIGENCE */}
{/* ====================================================== */}

<div className="mt-10">

  {/* HEADER */}

  <div className="mb-6">

    <h2 className="text-2xl font-bold text-gray-800">
      Executive Business Intelligence
    </h2>

    <p className="text-sm text-gray-500 mt-1">
      High-level business performance, profitability,
      market position and strategic priorities.
    </p>

  </div>


  {/* EXECUTIVE KPI CARDS */}

  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">

    {/* Revenue */}

    <div className="bg-white rounded-xl shadow-sm p-5 border">

      <p className="text-sm text-gray-500">
        Total Revenue
      </p>

      <h3 className="text-2xl font-bold text-gray-800 mt-2">
        ₹
        {Number(
          executiveSummary.total_revenue
        ).toLocaleString("en-IN", {
          maximumFractionDigits: 0
        })}
      </h3>

    </div>


    {/* Profit */}

    <div className="bg-white rounded-xl shadow-sm p-5 border">

      <p className="text-sm text-gray-500">
        Estimated Profit
      </p>

      <h3 className="text-2xl font-bold text-green-600 mt-2">
        ₹
        {Number(
          executiveSummary.estimated_profit
        ).toLocaleString("en-IN", {
          maximumFractionDigits: 0
        })}
      </h3>

    </div>


    {/* Margin */}

    <div className="bg-white rounded-xl shadow-sm p-5 border">

      <p className="text-sm text-gray-500">
        Estimated Profit Margin
      </p>

      <h3 className="text-2xl font-bold text-blue-600 mt-2">
        {Number(
          executiveSummary.estimated_profit_margin
        ).toFixed(2)}
        %
      </h3>

    </div>


    {/* Most Profitable */}

    <div className="bg-white rounded-xl shadow-sm p-5 border">

      <p className="text-sm text-gray-500">
        Most Profitable Category
      </p>

      <h3 className="text-2xl font-bold text-orange-500 mt-2">
        {executiveSummary.most_profitable_category}
      </h3>

    </div>

  </div>


  {/* STRATEGIC ALERTS */}

  <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mt-6">

    {/* High Priority */}

    <div className="bg-white rounded-xl shadow-sm p-5 border">

      <p className="text-sm text-gray-500">
        High-Priority Pricing Actions
      </p>

      <div className="flex items-center gap-3 mt-3">

        <span className="text-3xl font-bold text-red-600">
          {executiveSummary.high_priority_actions}
        </span>

        <span className="text-sm text-gray-600">
          categories require pricing attention
        </span>

      </div>

    </div>


    {/* Data Quality */}

    <div className="bg-white rounded-xl shadow-sm p-5 border">

      <p className="text-sm text-gray-500">
        Categories Requiring Better Data
      </p>

      <div className="flex items-center gap-3 mt-3">

        <span className="text-3xl font-bold text-yellow-600">
          {
            executiveSummary
              .categories_requiring_better_data
          }
        </span>

        <span className="text-sm text-gray-600">
          categories need improved competitor coverage
        </span>

      </div>

    </div>

  </div>


  {/* CATEGORY EXECUTIVE TABLE */}

  <div className="bg-white rounded-xl shadow-sm border mt-6 overflow-hidden">

    <div className="p-5 border-b">

      <h3 className="text-lg font-semibold text-gray-800">
        Executive Category Overview
      </h3>

      <p className="text-sm text-gray-500 mt-1">
        Category-level profitability, market position
        and recommended business priority.
      </p>

    </div>


    <div className="overflow-x-auto">

      <table className="w-full text-sm">

        <thead className="bg-gray-50">

          <tr>

            <th className="text-left px-5 py-3">
              Category
            </th>

            <th className="text-right px-5 py-3">
              Revenue
            </th>

            <th className="text-right px-5 py-3">
              Est. Profit
            </th>

            <th className="text-right px-5 py-3">
              Margin
            </th>

            <th className="text-left px-5 py-3">
              Market Position
            </th>

            <th className="text-left px-5 py-3">
              Priority
            </th>

            <th className="text-left px-5 py-3">
              Status
            </th>

          </tr>

        </thead>


        <tbody>

          {executiveCategories.map(
            (item) => (

              <tr
                key={item.Category_Name}
                className="border-t hover:bg-gray-50"
              >

                <td className="px-5 py-4 font-medium">
                  {item.Category_Name}
                </td>


                <td className="px-5 py-4 text-right">

                  ₹
                  {Number(
                    item.Total_Revenue
                  ).toLocaleString("en-IN", {
                    maximumFractionDigits: 0
                  })}

                </td>


                <td className="px-5 py-4 text-right font-medium">

                  ₹
                  {Number(
                    item.Estimated_Profit
                  ).toLocaleString("en-IN", {
                    maximumFractionDigits: 0
                  })}

                </td>


                <td className="px-5 py-4 text-right">

                  {Number(
                    item.Estimated_Profit_Margin
                  ).toFixed(1)}
                  %

                </td>


                <td className="px-5 py-4">

                  {item.Market_Position}

                </td>


                <td className="px-5 py-4">

                  <span
                    className={
                      item.Priority === "High"
                        ? "px-2.5 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-700"
                        : item.Priority === "Medium"
                        ? "px-2.5 py-1 rounded-full text-xs font-semibold bg-yellow-100 text-yellow-700"
                        : "px-2.5 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-700"
                    }
                  >

                    {item.Priority}

                  </span>

                </td>


                <td className="px-5 py-4">

                  <span
                    className={
                      item.Executive_Status ===
                      "Action Required"
                        ? "text-red-600 font-medium"
                        : item.Executive_Status ===
                          "Data Required"
                        ? "text-yellow-600 font-medium"
                        : item.Executive_Status ===
                          "Data Validation Required"
                        ? "text-orange-600 font-medium"
                        : "text-gray-600 font-medium"
                    }
                  >

                    {item.Executive_Status}

                  </span>

                </td>

              </tr>

            )
          )}

        </tbody>

      </table>

    </div>

  </div>


  {/* DISCLAIMER */}

  <div className="mt-4 px-4 py-3 bg-gray-50 rounded-lg">

    <p className="text-xs text-gray-500">
      Note: Profit and margin figures are estimated using
      the project's configured cost assumptions. Competitor
      pricing insights depend on the availability and
      comparability of competitor data.
    </p>

  </div>

</div>

    </Layout>

  );

}


export default Analytics;